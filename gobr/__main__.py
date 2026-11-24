"""CLI.

  python -m gobr contexto <dir_ou_arquivo_gobr> <dir_saida>     pacote JSON completo por arquivo
  python -m gobr entrada <dir_contexto> <dir_saida>             visão do pacote que o redator lê
  python -m gobr consolidar <dir_candidatos> <dir_saida> --contexto <dir> [<dir>...] --prompt <arquivo>
        valida os candidatos <dir_candidatos>/<arquivo>/*.json, escolhe o de maior concordância e
        grava <arquivo>.json (com _meta) e <arquivo>.md
  python -m gobr pendentes <dir_candidatos> <dir_entrada> --contexto <dir> [<dir>...]
        estratégia adaptativa: imprime "<arquivo> <n>" para cada arquivo que ainda precisa de n réplicas
        (completa até --base; vai até --maximo quando a concordância fica abaixo de --limiar)
  python -m gobr cobertura <dir_gobr>                            lista trechos não reconhecidos
  python -m gobr manual <manual.pdf> <dir_saida>                 seções e chunks do manual (exige pdfplumber)
  python -m gobr indexar-manual <dir_manual> <dir_indice> [--modelo M]   embute os chunks do manual
  python -m gobr buscar-manual <dir_indice> "<pergunta>" [-k 3] [--modo denso|bm25|hibrido]
  python -m gobr avaliar-manual <dir_indice> --consultas <arquivo.json> [-k 5]   Recall@1/@k e MRR por modo
  python -m gobr indexar <dir_descricoes> <dir_indice> --contexto <dir> [<dir>...] --gobr <dir> [<dir>...]
        embute os chunks (arquivo, regra, consulta hipotética) com --modelo e grava vetores e metadados
  python -m gobr buscar <dir_indice> "<descrição do usuário>" [-k 5]
        arquivos mais parecidos, um por assinatura estrutural, com o caminho do .gobr
  python -m gobr avaliar-indice <dir_indice> --consultas <arquivo.json> [<arquivo.json>...]
        Recall@1/@k e MRR por variante de índice (consultas: {arquivo esperado: texto})
  python -m gobr agente ["<mensagem>"] [--conversa NOME] [--memoria BANCO.db] [--servidor URL] [--manual-inteiro]
        conversa no terminal, com memória: o agente busca exemplos e manual, pode perguntar, e o .gobr entregue
        passa pelo validador (pacote) e pelo conferente de significado. Depois da resposta, cada linha é um novo
        turno (mudar, perguntar, desfazer, pedido novo); linha vazia ou /sair encerra, /memoria mostra o que está
        guardado. Com --conversa, retoma de onde parou, até no meio de uma pergunta
  python -m gobr conversas [--memoria BANCO.db]   Conversas guardadas
  python -m gobr avaliar-memoria <casos.json> <dir_saida> [--modo memoria|concatenada|nenhuma]
        roda as conversas roteirizadas e confere as saídas esperadas de cada turno
  python -m gobr avaliar-agente --consultas <arquivo.json> --gabaritos <dir_gobr> <dir_saida> [--manual-inteiro]
        roda o agente em cada consulta sem o próprio gabarito na busca (perguntas recebem a resposta padrão)
  python -m gobr avaliar-perguntas <casos.json> <dir_saida> [--manual-inteiro]
        roda o agente em cada caso com o usuário simulado do arquivo; mede se perguntou quando faltava algo
  python -m gobr conferir <arquivo.gobr> [<arquivo.gobr>...] --consultas <arquivo.json>
        só o conferente: compara o que cada regra faz com o pedido de mesmo nome em --consultas
"""
import argparse
import json
import sys
import time
from pathlib import Path

from gobr import consensus, redator
from gobr.context import build
from gobr.parser import parse_file, read_source, unrecognized

MODEL = "claude-sonnet-5-5"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-0.6B"
REPO = Path(__file__).resolve().parent.parent
EXAMPLES_INDEX = REPO / "data" / "indice" / "qwen3-0.6b"
MANUAL_INDEX = REPO / "data" / "indice_manual" / "qwen3-0.6b"
MEMORY_DB = REPO / "data" / "memoria" / "conversas.db"
LLM_SERVER = "http://127.0.0.1:8080/v1"  # llama-server local


def gobr_files(target: Path) -> list[Path]:
    files = [target] if target.is_file() else sorted(target.glob("*.gobr"))
    if not files:
        raise SystemExit(f"nenhum .gobr encontrado em {target}")
    return files


def write_json(path: Path, data: dict, indent: int | None = 2) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")


def write_packages(target: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = gobr_files(target)
    for path in paths:
        write_json(out_dir / f"{path.stem}.json", build(path))
    print(f"{len(paths)} pacotes gravados em {out_dir}")


def write_views(context_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    packages = sorted(context_dir.glob("*.json"))
    for path in packages:
        write_json(out_dir / path.name, redator.view(json.loads(path.read_text(encoding="utf-8"))), indent=1)
    print(f"{len(packages)} entradas do redator gravadas em {out_dir}")


def load_package(name: str, context_dirs: list[Path]) -> dict:
    for directory in context_dirs:
        path = directory / f"{name}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    raise SystemExit(f"{name}: pacote de contexto não encontrado em {context_dirs}")


def evaluate(file_dir: Path, package: dict) -> tuple[list[consensus.Candidate], consensus.Candidate | None, float]:
    candidates = [consensus.load(p, package) for p in sorted(file_dir.glob("*.json"))]
    chosen, agreement = consensus.choose(candidates)
    return candidates, chosen, agreement


def consolidate(candidates_dir: Path, out_dir: Path, context_dirs: list[Path], prompt: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for file_dir in sorted(p for p in candidates_dir.iterdir() if p.is_dir()):
        package = load_package(file_dir.name, context_dirs)
        candidates, chosen, agreement = evaluate(file_dir, package)
        meta = consensus.provenance(package, candidates, chosen, agreement, prompt, MODEL)
        valid = sum(c.report.ok for c in candidates)
        shown = "sem medida" if agreement is None else f"{agreement:.2f}"
        print(f"{file_dir.name}: {valid}/{len(candidates)} válidos, concordância {shown}, escolhido {meta['escolhido']}")
        if chosen is None:
            write_json(out_dir / f"{file_dir.name}.falha.json", {"_meta": meta})
            continue
        write_json(out_dir / f"{file_dir.name}.json", {**chosen.answer, "_meta": meta})
        (out_dir / f"{file_dir.name}.md").write_text(redator.render_markdown(chosen.answer, package), encoding="utf-8")


def report_pending(candidates_dir: Path, inputs_dir: Path, context_dirs: list[Path],
                   base: int, maximum: int, threshold: float) -> None:
    total = 0
    for input_path in sorted(inputs_dir.glob("*.json")):
        file_dir = candidates_dir / input_path.stem
        existing = sorted(file_dir.glob("*.json")) if file_dir.exists() else []
        missing = base - len(existing)
        if missing <= 0 and len(existing) < maximum:
            candidates, _, agreement = evaluate(file_dir, load_package(input_path.stem, context_dirs))
            if agreement is None or agreement < threshold:
                missing = maximum - len(existing)
        if missing > 0:
            print(f"{input_path.stem} {missing}")
            total += missing
    print(f"{total} réplicas pendentes", file=sys.stderr)


def write_manual(pdf: Path, out_dir: Path) -> None:
    from gobr import manual

    sections = manual.extract(pdf)
    if not sections:
        raise SystemExit(f"{pdf}: nenhuma seção encontrada (o capítulo 1 precisa de um título em negrito)")
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "secoes.json", [
        {"secao": s.number, "titulo": s.title, "pagina": s.page, "caminho": s.path, "texto": manual.render(s)}
        for s in sections
    ], indent=1)
    found = manual.chunks(sections)
    (out_dir / "chunks.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in found),
                                          encoding="utf-8")
    print(f"{len(sections)} seções, {len(found)} chunks gravados em {out_dir}")


def build_manual_index(manual_dir: Path, out_dir: Path, model: str) -> None:
    from gobr import index, manual_search

    built, manifest = manual_search.build(manual_dir, index.Embedder(model))
    manual_search.save(built, manifest, out_dir)
    print(f"{len(built.chunks)} chunks do manual ({model}) gravados em {out_dir}")


def search_manual(index_dir: Path, text: str, k: int, mode: str) -> None:
    from gobr import index, manual_search

    loaded = manual_search.load(index_dir)
    vector = index.Embedder(loaded.model).queries([text])[0]
    for n, hit in enumerate(manual_search.search(loaded, text, vector, k, mode), 1):
        print(f"{n}. {hit['secao']} {hit['titulo']} (p. {hit['pagina']})  {hit['nota']:.4f}")
        preview = [line for line in hit["chunk"]["texto"].splitlines() if line.strip() and line != "```"][-1]
        print(f"   [{hit['chunk']['tipo']}] {preview[:160]}")


def evaluate_manual(index_dir: Path, query_file: Path, k: int) -> None:
    from gobr import index, manual_search

    loaded = manual_search.load(index_dir)
    queries = json.loads(query_file.read_text(encoding="utf-8"))["consultas"]
    table = manual_search.evaluate(loaded, index.Embedder(loaded.model), queries, k)
    print(f"modelo: {loaded.model}\n")
    print(f"| modo | consultas | n | recall@1 | recall@{k} | MRR |")
    print("|---|---|---|---|---|---|")
    for (mode, kind), row in table.items():
        print(f"| {mode} | {kind} | {row['n']} | {row['recall@1']:.3f} | {row[f'recall@{k}']:.3f} | {row['mrr']:.3f} |")


def report_coverage(target: Path) -> None:
    total = 0
    for path in gobr_files(target):
        file = parse_file(path)
        total += sum(len(b.all_clauses()) + len(b.unclassified) for b in file.blocks)
        for block_id, item in unrecognized(file):
            print(f"{path.name}\t{block_id}\t{getattr(item, 'text', item)}")
    print(f"{total} cláusulas analisadas", file=sys.stderr)


# gobr.index exige numpy e sentence-transformers; o resto da CLI roda só com a biblioteca padrão.
def build_index(descriptions_dir: Path, out_dir: Path, context_dirs: list[Path], gobr_dirs: list[Path], model: str) -> None:
    from gobr import index

    built = index.build(descriptions_dir, context_dirs, gobr_dirs, index.Embedder(model))
    index.save(built, out_dir)
    print(f"{len(built.files)} arquivos, {len(built.chunks)} chunks ({model}) gravados em {out_dir}")


def search(index_dir: Path, text: str, k: int) -> None:
    from gobr import index

    loaded = index.load(index_dir)
    query = index.Embedder(loaded.model).queries([text])[0]
    for n, hit in enumerate(index.search(loaded, query, index.numbers(text), k), 1):
        same = f" (+{len(hit['equivalentes'])} de mesma estrutura)" if hit["equivalentes"] else ""
        print(f"{n}. {hit['arquivo']}  {hit['nota']:.3f}{same}  {hit['gobr']}")
        if hit["regra_mais_parecida"]:
            print(f"   regra mais parecida: {hit['regra_mais_parecida']['texto'].splitlines()[-1]}")


def evaluate_index(index_dir: Path, query_files: list[Path], k: int) -> None:
    from gobr import index

    loaded = index.load(index_dir)
    labelled = {}
    for path in query_files:
        queries = json.loads(path.read_text(encoding="utf-8"))
        labelled[path.stem] = {name: text for name, text in queries.items() if not name.startswith("_")}
    table = index.evaluate(loaded, index.Embedder(loaded.model), labelled, k)
    print(f"modelo: {loaded.model}\n")
    print(f"| chunks | peso dos números | consultas | n | recall@1 | recall@{k} | MRR | posições |")
    print("|---|---|---|---|---|---|---|---|")
    for (variant, weight, group), row in table.items():
        positions = "" if row["posicoes"] is None else " ".join(str(p or "-") for p in row["posicoes"])
        print(f"| {variant} | {weight} | {group} | {row['n']} | {row['recall@1']:.3f} | {row[f'recall@{k}']:.3f} "
              f"| {row['mrr']:.3f} | {positions} |")


def agent_resources(server: str, whole_manual: bool, prompt_tokens: list[int] | None = None):
    from gobr import agent, index, manual_search

    examples, manual = index.load(EXAMPLES_INDEX), manual_search.load(MANUAL_INDEX)
    if examples.model != manual.model:
        raise SystemExit(f"os índices usam modelos diferentes: {examples.model} e {manual.model}")
    return agent.Resources(examples, manual, index.Embedder(examples.model), agent.openai_chat(server, prompt_tokens),
                           whole_manual)


def _read_line(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:  # entrada redirecionada e já lida: vale como "sem resposta" e encerra a conversa
        return ""


def run_agent(text: str, conversation: str, db: Path, server: str, whole_manual: bool) -> None:
    """Uma conversa no terminal: retoma o que ficou pendente e depois trata cada linha como um turno."""
    from gobr import agent, memory

    def answer(question: str) -> str:
        return _read_line(f"\n{question}\n> ")

    name = conversation or time.strftime("conversa-%Y%m%d-%H%M%S")
    again = f'python -m gobr agente --conversa "{name}"' + ("" if db == MEMORY_DB else f' --memoria "{db}"')
    with agent.open_memory(db) as saver:
        graph = agent.build_graph(agent_resources(server, whole_manual), saver)
        print(f"Conversa: {name}", file=sys.stderr)
        try:
            # um turno que falhou só é refeito se não veio mensagem nova; uma pergunta pendente é sempre retomada
            pending = graph.get_state(agent.thread_config(name)).interrupts
            resumed = agent.converse(graph, None, answer, name) if pending or not text else None
            if resumed:
                print(resumed["resposta"])
            message = text or _read_line("\nVocê> ")
            while message.strip() and message.strip() != "/sair":
                if message.strip() == "/memoria":
                    print(memory.summary(graph.get_state(agent.thread_config(name)).values))
                else:
                    print(agent.converse(graph, {"mensagem": message}, answer, name)["resposta"])
                message = _read_line("\nVocê> ")
        except (Exception, KeyboardInterrupt) as exc:
            if not isinstance(exc, KeyboardInterrupt):
                print(f"\nErro: {type(exc).__name__}: {exc}", file=sys.stderr)
            raise SystemExit(f"A conversa está guardada. Para refazer este turno: {again}\n"
                             f'Para trocá-lo por outra mensagem: {again} "<mensagem>"') from exc
    print(f"Conversa guardada. Retome com: {again}", file=sys.stderr)


def list_conversations(db: Path) -> None:
    from gobr import agent

    if not db.exists():
        print("Nenhuma conversa guardada.")
        return
    with agent.open_memory(db) as saver:
        for c in agent.conversations(saver):
            print(f"{c['nome']}  {c['turnos']} turnos, versão {c['versao']}: {' '.join(c['inicio'].split())[:80]}")


def evaluate_memory(case_file: Path, out_dir: Path, mode: str, server: str, whole_manual: bool) -> None:
    """Verificações certas por caso; o banco fica em <saida>/conversas.db e cada rodada usa conversas novas."""
    from gobr import memory_eval

    tokens: list[int] = []
    resources = agent_resources(server, whole_manual, tokens)
    out_dir.mkdir(parents=True, exist_ok=True)
    run, totals = time.strftime("%Y%m%d-%H%M%S"), [0, 0]
    print("| caso | turnos | verificações certas | turnos todos certos | tipos | perguntas | maior prompt por turno (tokens) | s |")
    print("|---|---|---|---|---|---|---|---|")
    for name, turns in _read_cases(case_file).items():
        records = memory_eval.run_case(resources, turns, mode, out_dir / "conversas.db", f"{name}-{run}", tokens)
        (out_dir / f"{name}.md").write_text(memory_eval.case_report(name, records), encoding="utf-8")
        checks = [ok for r in records for _, ok in r["verificacoes"]]
        totals = [totals[0] + sum(checks), totals[1] + len(checks)]
        whole = sum(all(ok for _, ok in r["verificacoes"]) for r in records)
        print(f"| {name} | {len(records)} | {sum(checks)}/{len(checks)} | {whole}/{len(records)} "
              f"| {', '.join(r['tipo'] for r in records)} | {' '.join(str(r['perguntas']) for r in records)} "
              f"| {' '.join(str(r['tokens']) for r in records)} | {sum(r['segundos'] for r in records):.0f} |", flush=True)
    print(f"\nTotal ({mode}): {totals[0]}/{totals[1]} verificações")


def _read_cases(path: Path) -> dict:
    return {name: case for name, case in json.loads(path.read_text(encoding="utf-8")).items() if not name.startswith("_")}


def _run_case(graph, state: dict, answers: list[str], out_dir: Path, name: str) -> dict | None:
    """Roda uma conversa com respostas roteirizadas, grava .gobr e .md e devolve o estado final (None se falhou)."""
    from gobr import agent

    pending = list(answers)
    started = time.perf_counter()
    try:
        out = agent.converse(graph, state, lambda _question: pending.pop(0) if pending else agent.NO_ANSWER)
    except Exception as exc:  # servidor fora do ar, contexto estourado, laço: registra e segue para o próximo caso
        (out_dir / f"{name}.md").write_text(f"Erro: {type(exc).__name__}: {exc}", encoding="utf-8")
        print(f"| {name} | erro: {type(exc).__name__} |")
        return None
    out["segundos"] = time.perf_counter() - started
    (out_dir / f"{name}.gobr").write_bytes(out["gobr"].replace("\r\n", "\n").encode("utf-8"))
    (out_dir / f"{name}.md").write_text(out["resposta"], encoding="utf-8")
    return out


def evaluate_agent(query_file: Path, gold_dir: Path, out_dir: Path, server: str, whole_manual: bool) -> None:
    """Aprovado = sem erro de validação (parse, fontes, ações e números do pedido); o resto só é reportado."""
    from gobr import agent, index

    resources = agent_resources(server, whole_manual)
    queries = _read_cases(query_file)
    problems = [f"{n}: fora do índice" for n in queries if n not in resources.examples.files]
    problems += [f"{n}: sem {gold_dir / f'{n}.gobr'}" for n in queries if not (gold_dir / f"{n}.gobr").exists()]
    if problems:
        raise SystemExit("consultas sem gabarito utilizável: " + "; ".join(problems))
    graph = agent.build_graph(resources)
    out_dir.mkdir(parents=True, exist_ok=True)
    print("| gabarito | aprovado | entregas | passos | lacunas | perguntas (triagem + agente) | divergências (código + LLM) "
          "| regras (gerado/gabarito) | assinatura igual | alertas | s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for name, text in queries.items():
        out = _run_case(graph, {"mensagem": text, "excluir": [name]}, [], out_dir, name)
        if out is None:
            continue
        gold, made = build(gold_dir / f"{name}.gobr"), build(out_dir / f"{name}.gobr")
        print(f"| {name} | {'sim' if not out['erros'] else 'não'} | {out['entregas']} | {out['passos']} "
              f"| {len(out['lacunas_iniciais'])} | {_questions(out)} | {_divergences(out)} "
              f"| {len(made['regras'])}/{len(gold['regras'])} "
              f"| {'sim' if made['regras'] and index.signature(made) == index.signature(gold) else 'não'} "
              f"| {len(out['alertas']) + len(out['avisos'])} | {out['segundos']:.0f} |")


def _questions(out: dict) -> str:
    return f"{1 if out.get('pergunta_lacunas') else 0} + {len(out['perguntas'])}"


def _divergences(out: dict) -> str:
    by_code = len(out["divergencias_codigo"])
    return f"{by_code} + {len(out['divergencias']) - by_code}"


def evaluate_questions(case_file: Path, out_dir: Path, server: str, whole_manual: bool) -> None:
    """Cada caso: {"pedido", "falta" (o que falta, ou "" se está completo), "respostas" do usuário simulado}."""
    from gobr import agent

    graph = agent.build_graph(agent_resources(server, whole_manual))
    out_dir.mkdir(parents=True, exist_ok=True)
    print("| caso | faltava algo | lacunas | perguntou | perguntas (triagem + agente) | aprovado | divergências (código + LLM) "
          "| alertas | s |")
    print("|---|---|---|---|---|---|---|---|---|")
    for name, case in _read_cases(case_file).items():
        out = _run_case(graph, {"mensagem": case["pedido"]}, case["respostas"], out_dir, name)
        if out is not None:
            asked = out.get("pergunta_lacunas") or out["perguntas"]
            print(f"| {name} | {'sim' if case['falta'] else 'não'} | {len(out['lacunas_iniciais'])} "
                  f"| {'sim' if asked else 'não'} | {_questions(out)} | {'sim' if not out['erros'] else 'não'} "
                  f"| {_divergences(out)} | {len(out['alertas']) + len(out['avisos'])} | {out['segundos']:.0f} |")


def confer_files(paths: list[Path], query_file: Path, server: str) -> None:
    from gobr import agent

    queries, chat = _read_cases(query_file), agent.openai_chat(server)
    missing = [p.stem for p in paths if p.stem not in queries]
    if missing:
        raise SystemExit(f"sem pedido em {query_file}: {', '.join(missing)}")
    for path in paths:
        divergences, alerts = agent.confer(chat, read_source(path), queries[path.stem])
        print(f"## {path}\n\n" + "\n".join(f"- {d}" for d in divergences + alerts or ["confere"]) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m gobr")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("contexto", "entrada"):
        cmd = commands.add_parser(name)
        cmd.add_argument("entrada", type=Path)
        cmd.add_argument("saida", type=Path)
    consolidate_cmd = commands.add_parser("consolidar")
    consolidate_cmd.add_argument("candidatos", type=Path)
    consolidate_cmd.add_argument("saida", type=Path)
    consolidate_cmd.add_argument("--contexto", type=Path, nargs="+", required=True)
    consolidate_cmd.add_argument("--prompt", type=Path, required=True)
    pending_cmd = commands.add_parser("pendentes")
    pending_cmd.add_argument("candidatos", type=Path)
    pending_cmd.add_argument("entrada", type=Path)
    pending_cmd.add_argument("--contexto", type=Path, nargs="+", required=True)
    pending_cmd.add_argument("--base", type=int, default=3)
    pending_cmd.add_argument("--maximo", type=int, default=5)
    pending_cmd.add_argument("--limiar", type=float, default=0.8)
    manual_cmd = commands.add_parser("manual")
    manual_cmd.add_argument("pdf", type=Path)
    manual_cmd.add_argument("saida", type=Path)
    manual_index_cmd = commands.add_parser("indexar-manual")
    manual_index_cmd.add_argument("manual", type=Path)
    manual_index_cmd.add_argument("saida", type=Path)
    manual_index_cmd.add_argument("--modelo", default=EMBEDDING_MODEL)
    manual_search_cmd = commands.add_parser("buscar-manual")
    manual_search_cmd.add_argument("indice", type=Path)
    manual_search_cmd.add_argument("texto")
    manual_search_cmd.add_argument("-k", type=int, default=3)
    manual_search_cmd.add_argument("--modo", choices=("denso", "bm25", "hibrido"), default="hibrido")
    manual_eval_cmd = commands.add_parser("avaliar-manual")
    manual_eval_cmd.add_argument("indice", type=Path)
    manual_eval_cmd.add_argument("--consultas", type=Path, required=True)
    manual_eval_cmd.add_argument("-k", type=int, default=5)
    coverage_cmd = commands.add_parser("cobertura")
    coverage_cmd.add_argument("entrada", type=Path)
    index_cmd = commands.add_parser("indexar")
    index_cmd.add_argument("descricoes", type=Path)
    index_cmd.add_argument("saida", type=Path)
    index_cmd.add_argument("--contexto", type=Path, nargs="+", required=True)
    index_cmd.add_argument("--gobr", type=Path, nargs="+", required=True)
    index_cmd.add_argument("--modelo", default=EMBEDDING_MODEL)
    search_cmd = commands.add_parser("buscar")
    search_cmd.add_argument("indice", type=Path)
    search_cmd.add_argument("texto")
    search_cmd.add_argument("-k", type=int, default=5)
    eval_cmd = commands.add_parser("avaliar-indice")
    eval_cmd.add_argument("indice", type=Path)
    eval_cmd.add_argument("--consultas", type=Path, nargs="+", required=True)
    eval_cmd.add_argument("-k", type=int, default=5)
    agent_cmd = commands.add_parser("agente")
    agent_cmd.add_argument("texto", nargs="?", default="")
    agent_cmd.add_argument("--conversa", default="")
    list_cmd = commands.add_parser("conversas")
    for cmd in (agent_cmd, list_cmd):
        cmd.add_argument("--memoria", type=Path, default=MEMORY_DB)
    memory_cmd = commands.add_parser("avaliar-memoria")
    memory_cmd.add_argument("casos", type=Path)
    memory_cmd.add_argument("saida", type=Path)
    memory_cmd.add_argument("--modo", choices=("memoria", "concatenada", "nenhuma"), default="memoria")
    agent_eval_cmd = commands.add_parser("avaliar-agente")
    agent_eval_cmd.add_argument("saida", type=Path)
    agent_eval_cmd.add_argument("--consultas", type=Path, required=True)
    agent_eval_cmd.add_argument("--gabaritos", type=Path, required=True)
    questions_cmd = commands.add_parser("avaliar-perguntas")
    questions_cmd.add_argument("casos", type=Path)
    questions_cmd.add_argument("saida", type=Path)
    confer_cmd = commands.add_parser("conferir")
    confer_cmd.add_argument("arquivos", type=Path, nargs="+")
    confer_cmd.add_argument("--consultas", type=Path, required=True)
    confer_cmd.add_argument("--servidor", default=LLM_SERVER)
    for cmd in (agent_cmd, agent_eval_cmd, questions_cmd, memory_cmd):
        cmd.add_argument("--servidor", default=LLM_SERVER)
        cmd.add_argument("--manual-inteiro", action="store_true")
    args = parser.parse_args()
    if getattr(args, "k", 1) < 1:
        parser.error("-k precisa ser pelo menos 1")
    if args.command == "contexto":
        write_packages(args.entrada, args.saida)
    elif args.command == "entrada":
        write_views(args.entrada, args.saida)
    elif args.command == "consolidar":
        consolidate(args.candidatos, args.saida, args.contexto, args.prompt)
    elif args.command == "pendentes":
        report_pending(args.candidatos, args.entrada, args.contexto, args.base, args.maximo, args.limiar)
    elif args.command == "manual":
        write_manual(args.pdf, args.saida)
    elif args.command == "indexar-manual":
        build_manual_index(args.manual, args.saida, args.modelo)
    elif args.command == "buscar-manual":
        search_manual(args.indice, args.texto, args.k, args.modo)
    elif args.command == "avaliar-manual":
        evaluate_manual(args.indice, args.consultas, args.k)
    elif args.command == "cobertura":
        report_coverage(args.entrada)
    elif args.command == "indexar":
        build_index(args.descricoes, args.saida, args.contexto, args.gobr, args.modelo)
    elif args.command == "buscar":
        search(args.indice, args.texto, args.k)
    elif args.command == "agente":
        run_agent(args.texto, args.conversa, args.memoria, args.servidor, args.manual_inteiro)
    elif args.command == "conversas":
        list_conversations(args.memoria)
    elif args.command == "avaliar-memoria":
        evaluate_memory(args.casos, args.saida, args.modo, args.servidor, args.manual_inteiro)
    elif args.command == "avaliar-agente":
        evaluate_agent(args.consultas, args.gabaritos, args.saida, args.servidor, args.manual_inteiro)
    elif args.command == "avaliar-perguntas":
        evaluate_questions(args.casos, args.saida, args.servidor, args.manual_inteiro)
    elif args.command == "conferir":
        confer_files(args.arquivos, args.consultas, args.servidor)
    else:
        evaluate_index(args.indice, args.consultas, args.k)


if __name__ == "__main__":
    main()
