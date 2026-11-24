"""Avaliação da memória: conversas roteirizadas, com as saídas esperadas de cada turno conferidas em código."""
import json
import re
import time
from pathlib import Path

from gobr import agent, memory
from gobr.index import numbers
from gobr.text import fold

CHECKS = ("regras", "sem_regra", "intactas", "numero_ausente", "numero_presente", "arquivo_do_turno", "arquivo_difere_do_turno",
          "resposta_tem", "perguntas_max", "bloqueia_antes")
NAME_PREFIX = re.compile(r"^((regra \d+|clientes?|nao agendar|bloqueio|bloquear|de)\b[:\s-]*)+")


def _rules(gobr: str) -> list[dict]:
    """Nome, dias, ação, números e cláusulas (com as fontes) de cada regra do arquivo."""
    if not gobr:
        return []
    file, _ = agent._package(gobr)
    found = []
    for block in file.of_kind("parametros"):
        clauses = memory.clauses_with_sources(block, file.blocks)
        found.append({"nome": NAME_PREFIX.sub("", fold(block.name)), "dias": agent._frequency_days(block),
                      "acao": "nao_agendar" if block.schedules_nothing else "agendar",
                      "numeros": {n for text in clauses for n in numbers(text)}, "clausulas": clauses})
    return found


def _named(rules: list[dict], name: str) -> list[dict]:
    """Regras do segmento: o nome igual (com ou sem o plural) ou, na falta, as que começam por ele."""
    stem = re.escape(fold(name).removesuffix("s"))
    exact = [r for r in rules if re.fullmatch(rf"{stem}s?", r["nome"])]
    return exact or [r for r in rules if re.match(rf"{stem}s?\b", r["nome"])]


def check_turn(expected: dict, gobr: str, answer: str, questions: int, previous: list[str],
               failed: bool = False) -> list[tuple[str, bool]]:
    """Cada verificação do turno e se passou. `previous` traz o arquivo ao fim de cada turno anterior.

    Num turno que falhou (erro do validador ou exceção) nada passa: o arquivo que sobrou é o do turno anterior.
    """
    unknown = set(expected) - set(CHECKS)
    if unknown:
        raise ValueError(f"verificações desconhecidas no caso: {sorted(unknown)}")
    rules = _rules(gobr)
    before = _rules(previous[-1]) if previous else []
    results = []
    for name, wanted in expected.get("regras", {}).items():
        found = _named(rules, name)
        ok = bool(found) and all(
            ("dias" not in wanted or wanted["dias"] in r["dias"]) and ("acao" not in wanted or wanted["acao"] == r["acao"])
            and ("numero" not in wanted or wanted["numero"] in r["numeros"]) for r in found)
        results.append((f"{name}: {json.dumps(wanted)}", ok))
    for name in expected.get("sem_regra", []):
        results.append((f"sem regra {name}", bool(rules) and not _named(rules, name)))
    for name in expected.get("intactas", []):
        old, new = ([r["clausulas"] for r in _named(side, name)] for side in (before, rules))
        results.append((f"{name} intacta", bool(old) and old == new))
    for number in expected.get("numero_ausente", []):
        results.append((f"sem o {number}", bool(rules) and all(number not in r["numeros"] for r in rules)))
    for number in expected.get("numero_presente", []):
        results.append((f"com o {number}", any(number in r["numeros"] for r in rules)))
    if "arquivo_do_turno" in expected:
        turn = expected["arquivo_do_turno"]
        results.append((f"arquivo do turno {turn}", bool(gobr) and gobr == previous[turn - 1]))
    if "arquivo_difere_do_turno" in expected:
        turn = expected["arquivo_difere_do_turno"]
        results.append((f"arquivo difere do turno {turn}", bool(gobr) and gobr != previous[turn - 1]))
    for piece in expected.get("resposta_tem", []):
        results.append((f"resposta tem {piece}", memory.mentioned(piece, [], answer)))
    late = {NAME_PREFIX.sub("", fold(name)) for name in agent.late_blocks(gobr)} if gobr else set()
    for name in expected.get("bloqueia_antes", []):
        found = _named(rules, name)
        results.append((f"{name} bloqueia antes", bool(found) and not any(r["nome"] in late for r in found)))
    if "perguntas_max" in expected:
        results.append((f"até {expected['perguntas_max']} perguntas", questions <= expected["perguntas_max"]))
    return [(label, ok and not failed) for label, ok in results]


def run_case(res: agent.Resources, turns: list[dict], mode: str, db: Path, thread: str, tokens: list[int]) -> list[dict]:
    """Roda a conversa. No modo memoria, cada turno reabre o banco, como um processo novo.

    `tokens` é a lista que o LLM enche com o tamanho de cada prompt; o maior do turno vai no registro.
    """
    files, said, records = [], [], []
    for turn in turns:
        answers = list(turn.get("respostas", []))
        given = []

        def answer(_question: str) -> str:
            reply = answers.pop(0) if answers else agent.NO_ANSWER
            if reply != agent.NO_ANSWER:
                given.append(reply)
            return reply

        said.append(turn["mensagem"])
        started, sent = time.perf_counter(), len(tokens)
        text = "\n".join(said) if mode == "concatenada" else turn["mensagem"]
        try:
            with agent.open_memory(db) as saver:
                graph = agent.build_graph(res, saver)
                out = agent.converse(graph, {"mensagem": text}, answer, thread if mode == "memoria" else None)
        except Exception as exc:  # servidor fora do ar, contexto estourado, laço: o turno conta como falha
            out = {"tipo": "erro", "resposta": f"Erro: {type(exc).__name__}: {exc}", "erros": ["exceção"]}
        said += given
        failed = bool(out["erros"])
        now = None if failed else memory.current(out)
        gobr = now["gobr"] if now else (files[-1] if files else "")
        questions = len(agent._answers(out))
        records.append({"mensagem": turn["mensagem"], "tipo": out["tipo"], "resposta": out["resposta"],
                        "perguntas": questions, "tokens": max(tokens[sent:], default=0),
                        "verificacoes": check_turn(turn["espera"], gobr, out["resposta"], questions, files, failed),
                        "segundos": time.perf_counter() - started})
        files.append(gobr)
    return records


def case_report(name: str, records: list[dict]) -> str:
    parts = [f"# {name}"]
    for n, r in enumerate(records, 1):
        parts.append(f"## Turno {n} ({r['tipo']}, {r['segundos']:.0f} s, {r['tokens']} tokens no maior prompt)\n\n"
                     f"**Usuário:** {r['mensagem']}\n\n**Agente:**\n\n{r['resposta']}\n\n**Verificações:**\n"
                     + "\n".join(f"- [{'x' if ok else ' '}] {label}" for label, ok in r["verificacoes"]))
    return "\n\n".join(parts) + "\n"
