"""Fluxo agêntico (LangGraph) com memória: o LLM decide buscas e perguntas; o grafo valida e confere toda entrega.

    receber --1º pedido--> triagem
           \\--já há pedido--> interpretar --mudança ou pedido novo--> triagem
                                          \\--dúvida--> explicar
                                          \\--volta--> desfazer

    triagem --lacunas--> perguntar_lacunas --resposta--> triagem
           \\--> preparar -> agente --tool_calls--> ferramentas --(pergunta)--> perguntar --> agente
                                     \\--texto--> validar --erro--> agente
                                                         \\--ok--> conferir --divergência na 1ª--> agente
                                                                            \\--> responder

    responder, explicar, desfazer e mudança que não deu para aplicar --> lembrar

O LLM só extrai, redige e escolhe ferramentas (CASCADE-FIRST): a triagem devolve os segmentos do pedido em
JSON e o código decide o que falta perguntar; quem diz se o .gobr está certo é o parser, e o que cada regra
faz vem do pacote de `gobr.context`. Na conferência, o código compara ação e frequência com os segmentos, e
o conferente (LLM) compara, em português, a tabela do pacote com o pedido. `chat` recebe mensagens no formato da API OpenAI e devolve a mensagem do assistente;
`openai_chat` liga ao llama-server, e os testes passam um LLM falso. Perguntas ao usuário pausam o grafo
com `interrupt()`; `converse` retoma com a resposta.

Cada conversa é um `thread_id`, e cada chamada de `converse` é um turno. Entre turnos só passam o pedido
vigente, as versões do arquivo e o registro dos turnos (`gobr.memory`); o resto do estado é zerado em `receber`.
"""
import json
import re
import sys
import tempfile
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from gobr import cascade, index, manual_search, memory
from gobr.context import LATE_BLOCK, build
from gobr.memory import requested_numbers
from gobr.parser import parse_file, read_source, unrecognized
from gobr.text import fold

EXAMPLES_K = 3
MANUAL_K = 3
MAX_STEPS = 8  # chamadas do agente com ferramentas; depois disso ele tem de entregar
MAX_DELIVERIES = 3
MAX_QUESTIONS = 2
ROOT = Path(__file__).resolve().parent.parent  # os caminhos do manifesto do índice são relativos à raiz
PROMPT = ROOT / "redator" / "prompt_agente.md"
CONFERENCE_PROMPT = ROOT / "redator" / "prompt_conferente.md"
TRIAGE_PROMPT = ROOT / "redator" / "prompt_triagem.md"
INTERPRET_PROMPT = ROOT / "redator" / "prompt_interprete.md"
EXPLAIN_PROMPT = ROOT / "redator" / "prompt_explicar.md"
ACTIONS = ("agendar", "nao_agendar", "indefinido")
RESIDUAL = re.compile(r"\b(demais|restantes?)\b")  # no nome do segmento: "os demais" não precisa de critério
GOBR_BLOCK = re.compile(r"```[ \t]*(?:gobr)?[ \t]*\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)
ASK = "perguntar_usuario"
NOTES_CHARS = 1200  # o que se mostra das notas; o LLM às vezes pensa alto antes delas
NOTES_HEADER = re.compile(r"^\W*(notas|premissas|observacoes|o que ficou de fora)\b", re.IGNORECASE)
# vocabulário largo: na dúvida, o pedido fala do time, e a premissa P11 não se aplica
TEAM = re.compile(r"\b(times?|carteiras?|equipes?|vendedor\w*|televendas|representantes?|supervisor\w*|extern[oa]s?|campo|sdrs?)\b")
TEAM_QUESTION = re.compile(r"\b(times?|carteiras?|equipes?)\b")
OTHER_TOPIC = re.compile(r"\b(compr\w*|recencia|dias|frequencia|inclu\w*|criterio|agendad\w*|bloque\w*)\b")
SCOPE = re.compile(r"\b(empresa|global|globais|grupo|vendedor\w*|lojas?|rede|filia\w*)\b")
FREQUENCY_QUESTION = re.compile(r"\b(frequencia|periodicidade|quantos em quantos|cada quantos)\b")
DEFAULT_TEAM = 'time "televendas":\n    vendedores todostelevendas ativados'
SAME_SCOPE = ("O pedido não fala de escopo de compra (empresa, grupo ou vendedor): use o mesmo escopo, o padrão, em todas as "
              "faixas (sem `global` e sem `do vendedor`). Prospect é sempre da empresa.")
P11 = (f"Premissa P11: o pedido não diz o time nem a carteira. Use este time em todas as regras, sem carteira, e não "
       f"pergunte sobre isso:\n{DEFAULT_TEAM}")
CONTEXT_CHARS = 80000  # ~25 mil tokens (3,2 caracteres por token, medidos: 3,6): cabe nos 32k com a resposta e as ferramentas
OMITTED = "[resultado antigo omitido para caber no contexto; busque de novo se precisar]"
NO_ANSWER = "Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi."
QUESTION_LIMIT = "Limite de perguntas atingido: siga com a premissa mais provável e diga nas notas qual foi."
FORMS = (  # (o que o LLM escreve, a forma dos exemplos); as duas geram a mesma condição no catálogo
    (re.compile(r"\batividade( global| do vendedor)? de (\d+) dias", re.IGNORECASE), r"recencia de positivacao\1 em \2 dias"),
    (re.compile(r"\bprospects d(a empresa|o vendedor)\b", re.IGNORECASE),
     lambda m: "no ciclo de vida prospect com " + {"a": "a empresa", "o": "o vendedor"}[m.group(1)[0].lower()]),
)
LAST_STEP = "Limite de buscas atingido: entregue agora o arquivo GoBR completo no bloco ```gobr."

TOOLS = [
    {"type": "function", "function": {
        "name": "buscar_exemplos",
        "description": "Busca regras GoBR reais parecidas com um trecho do pedido, cada uma com a sua descrição.",
        "parameters": {"type": "object", "properties": {"consulta": {"type": "string"}}, "required": ["consulta"]}}},
    {"type": "function", "function": {
        "name": "buscar_manual",
        "description": "Busca no manual oficial do GoBR as seções sobre uma cláusula ou um critério de cliente.",
        "parameters": {"type": "object", "properties": {"consulta": {"type": "string"}}, "required": ["consulta"]}}},
    {"type": "function", "function": {
        "name": ASK,
        "description": "Pergunta ao usuário quando falta ao pedido algo sem o qual a regra seria um chute, ou "
                       "quando a modelagem comercial tem um ponto falho que só ele decide.",
        "parameters": {"type": "object", "properties": {"pergunta": {"type": "string"}}, "required": ["pergunta"]}}},
]
CONFERENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "regras": {"type": "array", "items": {
            "type": "object",
            "properties": {"regra": {"type": "string"}, "trecho_do_pedido": {"type": "string"},
                           "confere": {"type": "boolean"}, "motivo": {"type": "string"}},
            "required": ["regra", "trecho_do_pedido", "confere", "motivo"]}},
        "sem_regra": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["regras", "sem_regra"],
}
TRIAGE_SCHEMA = {  # sem campos nulos: "não informado" é "", "indefinido" ou 0, e o código confere tudo
    "type": "object",
    "properties": {
        "segmentos": {"type": "array", "items": {
            "type": "object",
            "properties": {"segmento": {"type": "string"}, "trecho": {"type": "string"},
                           "criterio": {"type": "string"}, "acao": {"type": "string", "enum": list(ACTIONS)},
                           "frequencia_dias": {"type": "integer"}},
            "required": ["segmento", "trecho", "criterio", "acao", "frequencia_dias"]}},
    },
    "required": ["segmentos"],
}
INTERPRET_SCHEMA = {
    "type": "object",
    "properties": {
        "tipo": {"type": "string", "enum": list(memory.KINDS)},
        "versao": {"type": "integer"},
        "operacoes": {"type": "array", "items": {
            "type": "object",
            "properties": {"op": {"type": "string", "enum": ["alterar", "incluir", "remover"]},
                           "linha": {"type": "integer"}, "texto": {"type": "string"}},
            "required": ["op", "linha", "texto"]}},
    },
    "required": ["tipo", "versao", "operacoes"],
}

Chat = Callable[..., dict]  # chat(messages, tools=None, schema=None) -> mensagem do assistente


class State(TypedDict, total=False):
    # memória: passa de um turno para o outro
    pedido: list[str]  # o pedido vigente, linha a linha, com as mudanças e as respostas do usuário
    versoes: list[dict]  # arquivos aprovados: n, pai (de onde veio), pedido, segmentos, gobr, notas, fora, sem_resposta
    versao_atual: int
    turnos: list[dict]  # n, mensagem, tipo, resumo, perguntas, versao (a que o turno criou, ou 0)
    sem_resposta: list[str]  # lacunas que o usuário não resolveu: a triagem não pergunta de novo
    # o turno
    mensagem: str
    tipo: str  # inicial, sem_mudanca ou um de `memory.KINDS`
    base: int  # versão de onde parte a mudança (0 = começa do zero)
    mudancas: list[dict]  # no pedido: antes e depois de cada linha
    avisos_memoria: list[str]
    descricao: str  # o pedido deste turno, já com as mudanças
    excluir: list[str]  # arquivos (e os de mesma assinatura) fora da busca, para avaliar sem o gabarito
    exemplos: list[dict]  # busca inicial
    segmentos: list[dict]  # o pedido, segmento a segmento, segundo a triagem
    lacunas: list[str]  # o que falta nos segmentos (o código decide, não o LLM)
    lacunas_iniciais: list[str] | None
    pergunta_lacunas: str
    resposta_lacunas: str
    avisos: list[str]  # da triagem: lacunas sem resposta, triagem sem JSON
    divergencias_codigo: list[str]  # a parte das divergências que `match_segments` achou (para medir)
    mensagens: list[dict]
    gobr: str
    notas: str  # o que o LLM escreveu fora do bloco: o que ficou de fora e dúvidas para o usuário
    erros: list[str]
    alertas: list[str]
    divergencias: list[str]
    perguntas: list[dict]
    passos: int
    entregas: int
    conferencias: int
    valido: dict | None  # última entrega sem erro (gobr, notas, alertas): volta se a correção pedida falhar
    restaurada: bool
    perdoados: list[int]  # números que só estavam numa regra de cláusula inventada, tirada pelo código
    resposta: str


@dataclass
class Resources:
    examples: index.Index
    manual: manual_search.ManualIndex
    embedder: object  # documents/queries, como `index.Embedder`
    chat: Chat
    whole_manual: bool = False  # manda o manual inteiro na 1ª mensagem em vez das seções recuperadas


def openai_chat(base_url: str, prompt_tokens: list[int] | None = None) -> Chat:
    """LLM por uma API compatível com a da OpenAI (llama-server), determinístico e sem raciocínio.

    `prompt_tokens`, se dado, recebe o tamanho de cada prompt enviado (para medir o contexto).
    """
    from openai import OpenAI  # import tardio: os testes não precisam do cliente

    client = OpenAI(base_url=base_url, api_key="sem-chave")

    def chat(messages: list[dict], tools: list[dict] | None = None, schema: dict | None = None) -> dict:
        extra = {}
        if tools:
            extra["tools"] = tools
        if schema:
            extra["response_format"] = {"type": "json_schema",
                                        "json_schema": {"name": "resposta", "strict": True, "schema": schema}}
        reply = client.chat.completions.create(model="local", messages=messages, temperature=0, seed=0,
                                               max_tokens=3072, reasoning_effort="none", **extra)
        if prompt_tokens is not None and reply.usage:
            prompt_tokens.append(reply.usage.prompt_tokens)
        choice = reply.choices[0]
        if choice.finish_reason == "length":
            print("aviso: resposta do LLM cortada no limite de tokens", file=sys.stderr)
        message = {"role": "assistant", "content": choice.message.content or ""}
        if choice.message.tool_calls:
            message["tool_calls"] = [{"id": c.id, "type": "function",
                                      "function": {"name": c.function.name, "arguments": c.function.arguments}}
                                     for c in choice.message.tool_calls]
        elif not message["content"]:
            print("aviso: o LLM devolveu uma resposta vazia", file=sys.stderr)
        return message

    return chat


def excluded_chunks(examples: index.Index, names: list[str]) -> frozenset[int]:
    unknown = [n for n in names if n not in examples.files]
    if unknown:
        raise ValueError(f"arquivos fora do índice, não dá para excluí-los da busca: {', '.join(unknown)}")
    signatures = {examples.files[n]["assinatura"] for n in names}
    return frozenset(i for i, c in enumerate(examples.chunks) if examples.files[c["arquivo"]]["assinatura"] in signatures)


def find_examples(res: Resources, text: str, vector, excluded: list[str]) -> list[dict]:
    file_text = {c["arquivo"]: c["texto"] for c in res.examples.chunks if c["tipo"] == "arquivo"}
    hits = index.search(res.examples, vector, index.numbers(text), EXAMPLES_K,
                        exclude=excluded_chunks(res.examples, excluded))
    return [{"arquivo": h["arquivo"], "descricao": file_text[h["arquivo"]], "gobr": read_source(ROOT / h["gobr"]).strip()}
            for h in hits if h["gobr"]]


def find_sections(res: Resources, text: str, vector) -> list[dict]:
    return [{"secao": s["secao"], "texto": s["texto"]} for s in manual_search.search(res.manual, text, vector, MANUAL_K)]


def examples_text(examples: list[dict]) -> str:
    return "\n".join(f"<exemplo arquivo=\"{e['arquivo']}\">\nDescrição: {e['descricao']}\n```gobr\n{e['gobr']}\n```\n"
                     "</exemplo>" for e in examples) or "Nenhum exemplo encontrado."


def sections_text(sections: list[dict]) -> str:
    return "\n".join(f"<secao numero=\"{s['secao']}\">\n{s['texto']}\n</secao>" for s in sections) or "Nenhuma seção."


def parse_segments(content: str) -> tuple[list[dict], list[str]]:
    """Segmentos da triagem, com os campos forçados ao esquema; JSON ruim não trava, vira aviso."""
    try:
        items = json.loads(content)["segmentos"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return [], ["A triagem não respondeu em JSON; o pedido não foi conferido segmento a segmento."]
    segments = []
    for item in items if isinstance(items, list) else []:
        if not isinstance(item, dict) or not fold(str(item.get("segmento", ""))):
            continue
        try:
            days = max(int(item.get("frequencia_dias") or 0), 0)
        except (TypeError, ValueError, OverflowError):
            days = 0
        segments.append({"segmento": str(item["segmento"]).strip(), "trecho": str(item.get("trecho") or "").strip(),
                         "criterio": str(item.get("criterio") or "").strip(),
                         "acao": item.get("acao") if item.get("acao") in ACTIONS else "indefinido",
                         "frequencia_dias": days})
    if not segments:
        return [], ["A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento."]
    return segments, []


def gaps(segments: list[dict]) -> list[str]:
    """O que falta ao pedido para escrever as regras sem chutar; cada lacuna vira uma linha da pergunta."""
    found = []
    for s in segments:
        name = s["segmento"]
        if s["acao"] == "indefinido":
            found.append(f'"{name}": agendar ou não agendar?')
        elif s["acao"] == "agendar" and s["frequencia_dias"] <= 0:
            found.append(f'"{name}": de quantos em quantos dias agendar?')
        if not s["criterio"] and not RESIDUAL.search(fold(name)):
            found.append(f'"{name}": quem são esses clientes (o critério)?')
    return found


def receive(state: State) -> State:
    """Começo do turno: zera o trabalho do anterior e mantém só a memória."""
    first = not state.get("pedido")
    return {"tipo": "inicial" if first else "", "base": 0, "mudancas": [], "avisos_memoria": [],
            "descricao": state["mensagem"] if first else "\n".join(state["pedido"]),
            "exemplos": [], "segmentos": [], "lacunas": [], "lacunas_iniciais": None, "pergunta_lacunas": "",
            "resposta_lacunas": "", "avisos": [], "divergencias_codigo": [], "mensagens": [], "gobr": "", "notas": "",
            "erros": [], "alertas": [], "divergencias": [], "perguntas": [], "passos": 0, "entregas": 0,
            "conferencias": 0, "valido": None, "restaurada": False, "perdoados": [], "resposta": ""}


def after_receive(state: State) -> str:
    return "triagem" if state["tipo"] == "inicial" else "interpretar"


def _numbered(lines: list[str]) -> str:
    return "\n".join(f"{n}. {line}" for n, line in enumerate(lines, 1))


def _unchanged(reason: str) -> State:
    return {"tipo": "sem_mudanca", "resposta": f"Não mudei nada. {reason}"}


def _objection(read: dict, lines: list[str], message: str, segments: list[dict]) -> str:
    """Por que a 1ª leitura da mensagem é suspeita; vazio se não é."""
    if read["tipo"] == "duvida" and not memory.is_question(message):
        return ("A mensagem não tem pergunta nem pede explicação. Releia-a: se ela manda mudar, incluir, tirar ou bloquear algo, "
                "o tipo é \"alterar\", com as operações.")
    if read["tipo"] != "alterar":
        return ""
    _, changes, warnings = memory.apply_operations(lines, read["operacoes"], message)
    missed = memory.left_behind(segments, changes, message)
    if missed:
        return (f"A mensagem também cita {', '.join(f'{chr(34)}{m}{chr(34)}' for m in missed)}, e nenhuma operação mexe nisso. "
                "Releia-a: se a mudança vale para esse segmento, inclua a operação dele; se ele só foi citado como referência, "
                "repita as mesmas operações.")
    if changes or not warnings:
        return ""
    return ("O programa recusou todas as operações:\n" + "\n".join(f"- {w}" for w in warnings)
            + "\nReleia a mensagem e mude só o que ela pede. Se ela fala de um grupo que ainda não está no pedido, use "
              "\"incluir\" com uma linha para ele.")


def interpret_message(res: Resources, state: State) -> State:
    """O LLM diz o que a mensagem é e que linhas do pedido mudam; o código aplica as mudanças."""
    lines, message = state["pedido"], state["mensagem"]
    content = (f"<pedido>\n{_numbered(lines)}\n</pedido>\n"
               f"<conversa>\n{memory.history_text(state.get('turnos', []))}\n</conversa>\n"
               f"<mensagem>\n{message}\n</mensagem>")
    asked = [{"role": "system", "content": INTERPRET_PROMPT.read_text(encoding="utf-8")},
             {"role": "user", "content": content}]
    reply = res.chat(asked, schema=INTERPRET_SCHEMA)
    read = memory.parse_interpretation(reply["content"])
    if (objection := _objection(read, lines, message, (memory.current(state) or {}).get("segmentos", []))):  # uma 2ª leitura, com o motivo; o que vier vale
        reply = res.chat(asked + [reply, {"role": "user", "content": objection}], schema=INTERPRET_SCHEMA)
        read = memory.parse_interpretation(reply["content"])
    if read["tipo"] == "duvida":
        return {"tipo": "duvida"}
    if read["tipo"] == "desfazer":
        now = memory.current(state)
        before = now["pai"] if now else 0
        last = next((t for t in reversed(state["turnos"]) if t["tipo"] != "duvida"), None)
        if not read["versao"] and now and last and last["tipo"] in ("alterar", "novo") and not last["versao"]:
            return _unchanged(f"A última mudança não tinha entrado, e a versão {now['n']} continua valendo."
                              + (f' Para voltar mais, diga "volte para a versão {before}".' if before else ""))
        target = memory.version(state, read["versao"] or before)
        if target is None or target["n"] == now["n"]:
            return _unchanged("Não há essa versão anterior para voltar.")
        return {"tipo": "desfazer", "base": target["n"]}
    if read["tipo"] == "novo":
        new, _, warnings = memory.apply_operations([], read["operacoes"], message)
        new = new or memory.request_lines(message)
        return {"tipo": "novo", "descricao": "\n".join(new), "avisos_memoria": warnings}
    new, changes, warnings = memory.apply_operations(lines, read["operacoes"], message)
    if read["tipo"] != "alterar" or not changes or not new:
        reasons = ["Isso apagaria o pedido inteiro."] if changes else warnings
        return _unchanged("Não entendi que parte do pedido mudar. Diga o segmento e o valor novo, por exemplo "
                          '"troque os ativos para 15 dias".' + "".join(f"\n- {r}" for r in reasons))
    return {"tipo": "alterar", "base": state.get("versao_atual") or 0, "mudancas": changes,
            "descricao": "\n".join(new), "avisos_memoria": warnings}


def after_interpret(state: State) -> str:
    return {"duvida": "explicar", "desfazer": "desfazer", "sem_mudanca": "lembrar"}.get(state["tipo"], "triagem")


def _base(state: State) -> dict | None:
    """A versão que este turno muda; None quando ele começa do zero."""
    return memory.version(state, state["base"])


def _answers(state: State) -> list[tuple[str, str]]:
    asked = [(state["pergunta_lacunas"], state["resposta_lacunas"])] if state.get("pergunta_lacunas") else []
    return asked + [(p["pergunta"], p["resposta"]) for p in state.get("perguntas", [])]


def triage(res: Resources, state: State) -> State:
    request = state["descricao"]
    if state.get("resposta_lacunas"):
        request += f"\n<respostas_do_usuario>\n{state['pergunta_lacunas']}\n-> {state['resposta_lacunas']}\n" \
                   "</respostas_do_usuario>"
    reply = res.chat([{"role": "system", "content": TRIAGE_PROMPT.read_text(encoding="utf-8")},
                      {"role": "user", "content": request}], schema=TRIAGE_SCHEMA)
    segments, warnings = parse_segments(reply["content"])
    base = _base(state)
    if base:
        segments = memory.keep_segments(base["segmentos"], segments, state["mudancas"], state["mensagem"])
    found = gaps(segments)
    first = state["lacunas_iniciais"]
    return {"segmentos": segments, "lacunas": found, "lacunas_iniciais": found if first is None else first,
            "avisos": warnings}


def _asked_before(state: State) -> list[str]:
    return [] if state["tipo"] == "novo" else state.get("sem_resposta", [])  # pedido novo: as lacunas são outras


def _open_gaps(state: State) -> list[str]:
    """Lacunas que ainda não foram perguntadas num turno anterior."""
    return [g for g in state["lacunas"] if g not in _asked_before(state)]


def after_triage(state: State) -> str:
    return "perguntar_lacunas" if _open_gaps(state) and not state.get("pergunta_lacunas") else "preparar"


def ask_gaps(state: State) -> State:
    """Uma só pergunta, montada pelo código, com todas as lacunas; a resposta volta para a triagem."""
    question = ("Para escrever as regras sem chutar, faltam estes dados no pedido:\n"
                + "\n".join(f"- {g}" for g in _open_gaps(state)) + "\nResponda numa mensagem só.")
    answer = str(interrupt({"pergunta": question})).strip()
    return {"pergunta_lacunas": question, "resposta_lacunas": answer or NO_ANSWER}


def after_ask_gaps(state: State) -> str:
    return "preparar" if state["resposta_lacunas"] == NO_ANSWER else "triagem"


def segments_text(segments: list[dict]) -> str:
    def action(s: dict) -> str:
        if s["acao"] == "nao_agendar":
            return "não agendar"
        if s["acao"] == "agendar":
            return f"agendar a cada {s['frequencia_dias']} dias" if s["frequencia_dias"] else (
                "agendar (frequência não dada; premissa P10: se o grupo é só um atributo, como inadimplentes, não escreva "
                "regra para ele: sem bloqueio, esses clientes seguem a regra da faixa deles)")
        return "indefinida"
    return "\n".join(f'- "{s["segmento"]}" | critério: {s["criterio"] or "(não dado)"} | ação: {action(s)}'
                     for s in segments)


def change_context(state: State) -> str:
    """O que a memória põe na 1ª mensagem do agente quando o turno muda um arquivo que já existe."""
    base = _base(state)
    if base is None:
        return ""
    changes = "\n".join(f"- {memory.change_text(c)}" for c in state["mudancas"])
    return (f'<conversa>\n{memory.history_text(state["turnos"])}\n</conversa>\n'
            f'<arquivo_atual versao="{base["n"]}">\n{base["gobr"]}\n</arquivo_atual>\n'
            f"<notas_anteriores>\n{base['notas'] or '(nenhuma)'}\n</notas_anteriores>\n"
            f"<mudanca>\nO arquivo atual atende ao pedido anterior, e o pedido acima já tem a mudança. Altere no "
            f"arquivo atual só o que ela pede, mantenha as outras regras idênticas e na mesma ordem, e entregue o "
            f"arquivo completo. Um bloqueio novo (`nao agendar`) entra antes das regras de frequência. O usuário escreveu: {state['mensagem']}\nMudança no pedido:\n{changes}\n</mudanca>\n")


def _team_is_open(state: State) -> bool:
    """O usuário não falou de time nem de carteira (nem nas respostas), e ainda não há arquivo que os defina."""
    return _base(state) is None and not TEAM.search(fold(_said(state)))


def _answers_text(state: State) -> str:
    return "\n".join(a for _, a in _answers(state) if a != NO_ANSWER)


def _said(state: State) -> str:
    return f"{state['descricao']}\n{_answers_text(state)}"


def _scope_is_open(state: State) -> bool:
    text = re.sub(r"prospects?[^\n.;]*", " ", fold(_said(state)))  # prospect é da empresa por definição
    return _base(state) is None and not SCOPE.search(text)


def prepare(res: Resources, state: State) -> State:
    request = state["descricao"]
    text = "\n".join(c["depois"] for c in state["mudancas"] if c["depois"]) or request  # o que mudou guia a busca
    vector = res.embedder.queries([text])[0]
    examples = find_examples(res, text, vector, state.get("excluir", []))
    if res.whole_manual:
        sections = [{"secao": s["secao"], "texto": s["texto"]} for s in res.manual.sections.values()]
    else:
        sections = find_sections(res, text, vector)
    first = f"<pedido>\n{request}\n</pedido>\n{change_context(state)}"
    premises = [P11] * _team_is_open(state) + [SAME_SCOPE] * _scope_is_open(state)
    if premises:
        first += "<premissas>\n" + "\n".join(premises) + "\n</premissas>\n"
    if state.get("segmentos"):
        answered = f"\nO usuário respondeu: {state['resposta_lacunas']}" if state.get("resposta_lacunas") else ""
        first += (f"<segmentos>\nO pedido, segmento a segmento (com as respostas do usuário, se houve pergunta). "
                  f"Escreva uma regra por segmento, com o nome do segmento e estes valores.{answered}\n"
                  f"{segments_text(state['segmentos'])}\n</segmentos>\n")
    first += (f"<exemplos>\n{examples_text(examples)}\n</exemplos>\n"
              f"<manual>\n{sections_text(sections)}\n</manual>")
    unresolved = ("Lacuna do pedido sem resposta do usuário" if (state["resposta_lacunas"] or NO_ANSWER) == NO_ANSWER
                  else "Lacuna que a resposta do usuário não resolveu")
    warnings = state.get("avisos", []) + [f"{unresolved}: {g}" for g in state.get("lacunas", [])]
    return {"exemplos": examples, "avisos": warnings,
            "mensagens": [{"role": "system", "content": PROMPT.read_text(encoding="utf-8")},
                          {"role": "user", "content": first}]}


def fit_context(messages: list[dict], limit: int) -> list[dict]:
    """As mensagens que cabem no contexto: omite primeiro as buscas antigas, depois as entregas antigas.

    As duas primeiras (prompt e pedido) e as três últimas ficam sempre inteiras; o estado guarda tudo.
    """
    size = sum(len(m["content"]) for m in messages)
    fitted = list(messages)
    for roles in (("tool",), ("assistant",)):
        for n, message in enumerate(fitted[:-3]):
            if size <= limit:
                return fitted
            if n >= 2 and message["role"] in roles and len(message["content"]) > len(OMITTED):
                size -= len(message["content"]) - len(OMITTED)
                fitted[n] = {**message, "content": OMITTED}
    return fitted


def act(res: Resources, state: State) -> State:
    messages, steps = state["mensagens"], state["passos"] + 1
    if steps == MAX_STEPS:
        messages = messages + [{"role": "user", "content": LAST_STEP}]
    reply = res.chat(fit_context(messages, CONTEXT_CHARS), tools=TOOLS if steps < MAX_STEPS else None)
    if steps >= MAX_STEPS:  # sem ferramentas oferecidas, uma chamada mesmo assim conta como entrega (sem laço)
        reply = {k: v for k, v in reply.items() if k != "tool_calls"}
    return {"mensagens": messages + [reply], "passos": steps}


def after_act(state: State) -> str:
    return "ferramentas" if state["mensagens"][-1].get("tool_calls") else "validar"


def _arguments(call: dict) -> dict:
    try:
        args = json.loads(call["function"]["arguments"] or "{}")
    except json.JSONDecodeError:
        return {}
    return args if isinstance(args, dict) else {}


def _last_calls(state: State) -> list[dict]:
    return next(m for m in reversed(state["mensagens"]) if m["role"] == "assistant")["tool_calls"]


def run_tool(res: Resources, state: State, name: str, args: dict) -> str:
    query = str(args.get("consulta", "")).strip()
    if name not in ("buscar_exemplos", "buscar_manual"):
        return f"Ferramenta desconhecida: {name}."
    if not query:
        return "Argumento `consulta` vazio: diga o que buscar."
    vector = res.embedder.queries([query])[0]
    if name == "buscar_exemplos":
        return examples_text(find_examples(res, query, vector, state.get("excluir", [])))
    return sections_text(find_sections(res, query, vector))


def use_tools(res: Resources, state: State) -> State:
    results = [{"role": "tool", "tool_call_id": c["id"],
                "content": run_tool(res, state, c["function"]["name"], _arguments(c))}
               for c in _last_calls(state) if c["function"]["name"] != ASK]
    return {"mensagens": state["mensagens"] + results}


def after_tools(state: State) -> str:
    return "perguntar" if any(c["function"]["name"] == ASK for c in _last_calls(state)) else "agente"


def _answer_without_the_user(state: State, question: str) -> str | None:
    """Pergunta que uma premissa ou a pergunta da triagem já respondeu; None se é para o usuário."""
    text = fold(question)
    if _team_is_open(state) and TEAM_QUESTION.search(text) and not OTHER_TOPIC.search(text):
        return P11
    asked = state["lacunas_iniciais"] if state["pergunta_lacunas"] else _asked_before(state)
    still_open = {s["segmento"] for s in state["segmentos"] for g in state["lacunas"]
                  if g in (asked or []) and g.startswith(f'"{s["segmento"]}": de quantos')}
    if FREQUENCY_QUESTION.search(text) and any(memory.mentioned(n, [], question) for n in still_open):
        return f"Esta pergunta já foi feita ao usuário. Resposta: {state['resposta_lacunas'] or NO_ANSWER}"
    return None


def ask(state: State) -> State:
    """Pausa o grafo por pergunta; ao retomar, o nó roda de novo e cada `interrupt` devolve a sua resposta."""
    asked, results = list(state["perguntas"]), []
    for call in (c for c in _last_calls(state) if c["function"]["name"] == ASK):
        question = str(_arguments(call).get("pergunta", "")).strip()
        previous = next((p["resposta"] for p in asked if p["pergunta"] == question), None)
        if not question:
            answer = "Pergunta vazia: escreva a pergunta no argumento `pergunta`."
        elif previous is not None:  # a mesma pergunta de novo não incomoda o usuário: vale a resposta anterior
            answer = f"Você já fez esta pergunta. Resposta: {previous}"
        elif (known := _answer_without_the_user(state, question)) is not None:
            answer = known
        elif len(asked) >= MAX_QUESTIONS:
            answer = QUESTION_LIMIT
        else:
            answer = str(interrupt({"pergunta": question})).strip() or NO_ANSWER
            asked.append({"pergunta": question, "resposta": answer})
        results.append({"role": "tool", "tool_call_id": call["id"], "content": answer})
    return {"mensagens": state["mensagens"] + results, "perguntas": asked}


def strip_comments(gobr_text: str) -> str:
    """Tira as linhas `#` depois da primeira linha de código: no .gobr gerado, são o LLM pensando alto."""
    lines, kept, in_code = gobr_text.split("\n"), [], False
    for line in lines:
        is_comment = line.strip().startswith("#")
        if in_code and is_comment:
            continue
        in_code = in_code or (bool(line.strip()) and not is_comment)
        kept.append(line)
    return "\n".join(kept)


def _package(gobr_text: str):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rascunho.gobr"
        path.write_bytes(gobr_text.replace("\r\n", "\n").encode("utf-8"))  # \r conta como caractere de controle
        return parse_file(path), build(path)


def _clause_numbers(file) -> set[int]:
    return {n for b in file.blocks for c in b.all_clauses() for n in index.numbers(c.text)}


def check(gobr_text: str, description: str, notes: str = "", left_out_before: frozenset[int] = frozenset(),
          declared_only: bool = False) -> tuple[list[str], list[str]]:
    """Erros (o .gobr não serve e volta ao LLM) e alertas da cascata (pontos falhos para o usuário).

    Um número do pedido conta quando aparece numa cláusula (não no nome da regra) ou quando o LLM diz, nas
    notas, que o deixou de fora porque o GoBR não o expressa (ou disse num turno anterior: `left_out_before`).
    Com `declared_only`, só vale a linha das notas que diz isso com todas as letras: numa mudança, as notas contam o
    que mudou ("de 14 para 15"), e citar o número não é deixá-lo de fora.
    """
    if not gobr_text:
        return ["A resposta não trouxe um bloco ```gobr com o arquivo."], []
    file, package = _package(gobr_text)
    errors = [f"{block_id}: trecho não reconhecido: {getattr(item, 'text', item)}. Essa cláusula não existe no GoBR desse jeito. Se não "
              "souber a forma certa, procure com buscar_manual ou buscar_exemplos pelo critério e mantenha o filtro. Só se o GoBR "
              "não tiver cláusula para isso, tire o trecho e diga nas notas o que ficou de fora, com o número." for block_id, item in unrecognized(file)]
    for block in file.blocks:
        undeclared = sorted({n for c in block.sources for n in c.detail.get("fontes_nao_declaradas", [])})
        if undeclared:
            errors.append(f'"{block.name}": fonte não declarada no arquivo: {", ".join(undeclared)}.')
        if block.kind == "parametros" and not block.actions:
            errors.append(f'"{block.name}": regra sem ação (frequência, preferência ou nao agendar).')
    if not package["regras"]:
        errors.append("O arquivo não tem nenhuma regra `parametros`.")
    for rule in package["regras"]:  # num arquivo novo, regra que não pega nenhum cliente é sempre defeito
        if rule["condicao_propria"] is None:
            errors.append(f'"{rule["nome"]}": os filtros se contradizem, nenhum cliente atende a todos.')
        elif rule["inalcancavel"]:
            errors.append(f'"{rule["nome"]}": inalcançável, todos os clientes dela já foram tratados por regras anteriores.')
    for effective in cascade.compute(file):
        day = cascade.single_day(effective.own)
        if day is not None:
            errors.append(f'"{effective.block.name}": os filtros só deixam quem está há exatamente {day} dias, então quase '
                          f'ninguém. Para "comprou nos últimos {day} dias", fique só com o filtro de atividade ou recência; '
                          f'para "sem comprar há mais de {day} dias", só com o de inatividade.')
    absent = requested_numbers(description) - _clause_numbers(file)
    said_left_out = (memory.declared_left_out(notes) if declared_only else index.numbers(notes)) | left_out_before
    left_out = sorted(absent & said_left_out)
    missing = sorted(absent - said_left_out)
    if missing:
        errors.append(f"Números do pedido ausentes nas cláusulas do GoBR: {', '.join(map(str, missing))}. Ponha cada "
                      "um numa cláusula ou, se o GoBR não o expressa, diga depois do código o que ficou de fora, "
                      "com o número.")
    alerts = package["alertas"] + [f"{r['nome']}: {a}" for r in package["regras"] for a in r["alertas"]]
    if left_out:
        alerts.append(f"Números do pedido que ficaram de fora do GoBR (ver notas): {', '.join(map(str, left_out))}.")
    return errors, alerts


def _left_out_before(state: State) -> frozenset[int]:
    """Números que a versão de origem já deixou de fora, salvo os que a mudança voltou a pedir."""
    base = _base(state)
    asked_again = {n for c in state["mudancas"] for n in requested_numbers(c["depois"])}
    return (frozenset(base["fora"]) - asked_again if base else frozenset()) | frozenset(state["perdoados"])


def drop_rules(gobr_text: str, names: list[str]) -> str:
    """O arquivo sem os blocos `parametros` desses nomes."""
    blocks = _package(gobr_text)[0].blocks
    lines, dropped = gobr_text.split("\n"), set()
    for block, following in zip(blocks, blocks[1:] + [None]):
        if block.kind == "parametros" and block.name in names:
            dropped.update(range(block.line_no - 1, following.line_no - 1 if following else len(lines)))
    return "\n".join(line for n, line in enumerate(lines) if n not in dropped).strip() if dropped else gobr_text


def _prune_unknown(gobr: str, notes: str, state: State) -> State | None:
    """Na última entrega de um arquivo novo: sem as regras de cláusula inventada que o pedido não tem como segmento.

    Só poda quando há segmentos para comparar e a regra não tem nenhuma palavra em comum com eles.
    """
    if not gobr or not state["segmentos"] or _base(state):
        return None
    file, _ = _package(gobr)
    wanted = {w for s in state["segmentos"] for w in _stems(s["segmento"])}
    clauses: dict[str, list[str]] = {}
    for block_id, item in unrecognized(file):
        block = next(b for b in file.blocks if b.id == block_id)
        if block.kind != "parametros" or _stems(block.name) & wanted:
            return None
        clauses.setdefault(block.name, []).append(getattr(item, "text", item))
    if not clauses:
        return None
    left = drop_rules(gobr, list(clauses))
    used = {n for s in state["segmentos"] for n in index.numbers(f'{s["trecho"]} {s["criterio"]}') | {s["frequencia_dias"]}}
    forgiven = {n for texts in clauses.values() for t in texts for n in index.numbers(t)} - used
    errors, alerts = check(left, memory.binding_text(state["descricao"]), notes, _left_out_before(state) | forgiven)
    if errors:
        return None
    alerts += [f'Tirei a regra "{name}": a cláusula `{"; ".join(texts)}` não existe no GoBR, e o que ela pedia ficou de fora.'
               for name, texts in clauses.items()]
    return {"gobr": left, "alertas": alerts, "perdoados": sorted(forgiven)}


def _stems(name: str) -> set[str]:
    """Palavras do nome sem o plural e sem as que qualquer regra tem."""
    words = {w.removesuffix("s") for w in re.findall(r"[a-z]{3,}", fold(name))}
    return words - {"cliente", "nao", "agendar", "regra", "com", "dos", "das", "que", "para", "dia"}


def canonical_forms(gobr_text: str) -> str:
    """O arquivo com as cláusulas na forma dos exemplos do corpus; igual ao original se algo mudar de sentido."""
    parts = re.split(r'("[^"]*")', gobr_text)  # os textos entre aspas (nomes) não mudam
    for n in range(0, len(parts), 2):
        for pattern, form in FORMS:
            parts[n] = pattern.sub(form, parts[n])
    rewritten = "".join(parts)
    if rewritten == gobr_text:
        return gobr_text
    before, after = _package(gobr_text)[0], _package(rewritten)[0]

    def meaning(file):
        return [(e.block.name, e.boxes, [c.text for c in e.block.actions]) for e in cascade.compute(file)]

    same = meaning(before) == meaning(after) and len(unrecognized(after)) <= len(unrecognized(before))
    return rewritten if same else gobr_text


def validate(state: State) -> State:
    reply = state["mensagens"][-1]["content"]
    block = GOBR_BLOCK.search(reply)
    gobr = canonical_forms(strip_comments(block.group(1).strip())) if block else ""
    notes = ((reply[:block.start()] + reply[block.end():]) if block else reply).strip()
    errors, alerts = check(gobr, memory.binding_text(state["descricao"]), notes, _left_out_before(state),
                           declared_only=_base(state) is not None)
    deliveries = state["entregas"] + 1
    if errors and deliveries >= MAX_DELIVERIES and not state["valido"]:
        pruned = _prune_unknown(gobr, notes, state)
        if pruned:
            return {**pruned, "notas": notes, "erros": [], "entregas": deliveries,
                    "valido": {"gobr": pruned["gobr"], "notas": notes, "alertas": pruned["alertas"]}}
    if not errors:
        return {"gobr": gobr, "notas": notes, "erros": [], "alertas": alerts, "entregas": deliveries,
                "valido": {"gobr": gobr, "notas": notes, "alertas": alerts}}
    if deliveries >= MAX_DELIVERIES and state["valido"]:  # a correção pedida pelo conferente não passou
        kept = state["valido"]
        return {**kept, "erros": [], "entregas": deliveries, "restaurada": True,
                "alertas": kept["alertas"] + ["A correção pedida pelo conferente não passou no validador; "
                                              "esta é a última versão que passou."]}
    messages = state["mensagens"]
    if deliveries < MAX_DELIVERIES:
        messages = messages + [{"role": "user", "content": "O validador encontrou estes erros no arquivo que você "
                                "entregou. Corrija-os sem mexer no que estava certo e entregue o arquivo completo de "
                                "novo:\n" + "\n".join(f"- {e}" for e in errors)}]
    return {"gobr": gobr, "notas": notes, "erros": errors, "alertas": alerts, "entregas": deliveries,
            "mensagens": messages}


def after_validate(state: State) -> str:
    if state["restaurada"]:
        return "responder"  # a versão restaurada já foi conferida; as divergências dela continuam no estado
    if not state["erros"]:
        return "conferir"
    return "agente" if state["entregas"] < MAX_DELIVERIES else "responder"


def rule_table(gobr_text: str) -> str:
    """O que cada regra faz, segundo o pacote (cascata), em português: é o que o conferente compara."""
    _, package = _package(gobr_text)
    names = {r["id"]: r["nome"] for r in package["regras"]}
    lines = []
    for rule in package["regras"]:
        if rule["acao_principal"] == "nao_agendar":
            action = "não agendar"
        else:
            action = "; ".join(f"{a['codigo']} ({a['significado']})" if a["significado"] else a["codigo"]
                               for a in rule["acoes"]) or "nenhuma"
        clients = rule["condicao_efetiva"] or "nenhum cliente (regra inalcançável)"
        filters = " e ".join(f["codigo"] for f in rule["filtros"]) or "nenhum"
        blocked = ", ".join(f'"{names.get(b, b)}"' for b in rule["bloqueios_anteriores"]) or "nenhum"
        lines.append(f'- "{rule["nome"]}" | fonte: {rule["fonte"]} | filtros: {filters} | clientes: {clients} '
                     f'| já excluídos pelos bloqueios: {blocked} | ação: {action}')
    return "\n".join(lines)


def late_blocks(gobr_text: str) -> list[str]:
    """Regras `nao agendar` que vêm depois de regras de frequência que já trataram clientes delas."""
    return [r["nome"] for r in _package(gobr_text)[1]["regras"] if any(a.startswith(LATE_BLOCK) for a in r["alertas"])]


def _attribute_rules(gobr_text: str) -> list[cascade.Effective]:
    return [e for e in cascade.compute(_package(gobr_text)[0])
            if e.block.kind == "parametros" and not e.block.schedules_nothing and cascade.attribute_only(e)]


def late_attribute_rules(gobr_text: str, segments: list[dict]) -> list[str]:
    """Regras de frequência só de atributo que vêm depois de faixas de compra que já trataram clientes delas.

    Só julga o segmento que o pedido define sem nenhum número e que não é o resto ("demais"): em "Inativos curva A", a
    regra só de curva é o resto de uma faixa, forma comum no corpus (80 regras em 25 arquivos).
    """
    attributes = {e.block.id for e in _attribute_rules(gobr_text)}
    return [e.block.name for e in cascade.compute(_package(gobr_text)[0]) if e.block.id in attributes
            and any(not b.schedules_nothing and b.id not in attributes for b in e.treated_before)
            and (s := memory.segment_of(e.block.name, segments)) and not index.numbers(s["criterio"])
            and not RESIDUAL.search(fold(f'{s["segmento"]} {s["criterio"]}'))]


def invented_frequencies(gobr_text: str, segments: list[dict], answers: str = "") -> list[str]:
    """Regras só de atributo com dias que ninguém deu: o pedido manda agendar sem frequência (premissa P10).

    Fica a regra cujos dias estão numa resposta do usuário, a que não é em dias (histórico, dias úteis) e a de um
    arquivo sem faixas de compra que peguem os clientes dela.
    """
    rules = _attribute_rules(gobr_text)
    attributes = {e.block.id for e in rules}
    bands = [e for e in cascade.compute(_package(gobr_text)[0]) if e.block.kind == "parametros" and e.own
             and e.block.id not in attributes and not e.block.schedules_nothing]
    said = index.numbers(answers)
    return [e.block.name for e in rules if bands and (days := _frequency_days(e.block)) and not said & set(days)
            and (s := memory.segment_of(e.block.name, segments)) and s["acao"] == "agendar" and not s["frequencia_dias"]]


def _frequency_days(block) -> list[int]:
    days = []
    for clause in block.actions:
        if clause.detail.get("tipo") == "frequencia":
            m = re.match(r"frequencia de (\d+) dias?\b", fold(clause.text))  # 1ª opção de "... ou ..."
            days += [int(m.group(1))] if m else list(clause.detail.get("dias_equivalentes", []))
    return days


def match_segments(gobr_text: str, segments: list[dict]) -> list[str]:
    """Ação e frequência de cada regra contra o segmento de mesmo nome (ou nome que é prefixo do da regra).

    Regra sem segmento correspondente não é julgada aqui: os nomes variam, e o código não chuta.
    """
    if not gobr_text or not segments:
        return []
    file, package = _package(gobr_text)
    blocks = {b.id: b for b in file.blocks}
    found = []
    for rule in package["regras"]:
        seg = memory.segment_of(rule["nome"], segments)
        if seg is None or seg["acao"] == "indefinido":
            continue
        blocking = rule["acao_principal"] == "nao_agendar"
        if seg["acao"] == "agendar" and blocking:
            found.append(f'"{rule["nome"]}": o pedido manda agendar; a regra é não agendar.')
        elif seg["acao"] == "nao_agendar" and not blocking:
            found.append(f'"{rule["nome"]}": o pedido manda não agendar; a regra agenda.')
        elif seg["acao"] == "agendar" and seg["frequencia_dias"]:
            days = _frequency_days(blocks[rule["id"]])
            if days and seg["frequencia_dias"] not in days:
                found.append(f'"{rule["nome"]}": a regra agenda a cada {days[0]} dias; o pedido dá {seg["frequencia_dias"]}.')
    return found


def confer(chat: Chat, gobr_text: str, description: str, notes: str = "") -> tuple[list[str], list[str]]:
    """Divergências entre o pedido e o que as regras fazem, e alertas do próprio conferente."""
    content = (f"<pedido>\n{description}\n</pedido>\n<regras>\n{rule_table(gobr_text)}\n</regras>\n"
               f"<notas_do_redator>\n{notes or '(nenhuma)'}\n</notas_do_redator>")
    reply = chat([{"role": "system", "content": CONFERENCE_PROMPT.read_text(encoding="utf-8")},
                  {"role": "user", "content": content}], schema=CONFERENCE_SCHEMA)
    try:  # o conferente às vezes pensa alto dentro do campo `motivo`; na resposta, só cabe o começo
        data = json.loads(reply["content"])
        divergences = [f'"{r["regra"]}": {memory.short(r["motivo"])} (pedido: "{memory.short(r["trecho_do_pedido"])}")'
                       for r in data["regras"] if not r["confere"]]
        divergences += [f'Trecho do pedido sem regra: "{s}"' for s in data["sem_regra"]]
    except (json.JSONDecodeError, KeyError, TypeError):
        return [], ["O conferente não respondeu em JSON; o significado das regras não foi conferido."]
    return divergences, []


def conference(res: Resources, state: State) -> State:
    request = state["descricao"]  # o que o usuário respondeu também é pedido: o valor dado na conversa confere
    if _answers(state):
        request += "\nRespostas do usuário às perguntas do agente:\n" + "\n".join(
            f"- {q} -> {a}" for q, a in _answers(state))
    by_segment = match_segments(state["gobr"], state.get("segmentos", []))  # o código antes do LLM
    invented = invented_frequencies(state["gobr"], state["segmentos"], _answers_text(state))
    by_segment += [p10_divergence(name) for name in invented]
    base = _base(state)
    old_names = {fold(b.name) for b in _package(base["gobr"])[0].blocks} if base else set()
    by_segment += [f'"{name}": a regra vem depois de outras que já trataram clientes dela e quase não os pega. Ponha-a '
                   "antes das faixas de compra." for name in late_attribute_rules(state["gobr"], state["segmentos"])
                   if name not in invented and fold(name) not in old_names]
    without_frequency = [s["segmento"] for s in state["segmentos"] if s["acao"] == "agendar" and not s["frequencia_dias"]]
    if without_frequency:
        request += f"\nPremissa P10: {', '.join(without_frequency)} não tem frequência no pedido; se o grupo é definido " \
                   "só por um atributo (ex.: inadimplentes), não ter regra própria está certo."
    if base:
        by_segment += memory.untouched_changes(_package(base["gobr"])[0].blocks, _package(state["gobr"])[0].blocks,
                                               base["segmentos"], state["segmentos"], state["mudancas"],
                                               state["mensagem"])
        by_segment += [f'"{name}": o bloqueio novo ficou depois de regras de frequência e não pega os clientes que elas '
                       "já trataram. Ponha-o antes das regras de frequência."
                       for name in late_blocks(state["gobr"]) if fold(name) not in old_names]
    divergences, alerts = confer(res.chat, state["gobr"], request, state["notas"])
    divergences = by_segment + divergences
    count = state["conferencias"] + 1
    messages = state["mensagens"]
    if divergences and count == 1 and state["entregas"] < MAX_DELIVERIES:
        can_ask = state["passos"] + 1 < MAX_STEPS
        messages = messages + [{"role": "user", "content": "O conferente comparou o que cada regra do arquivo faz "
                                "com o pedido e achou estas divergências:\n" + "\n".join(f"- {d}" for d in divergences)
                                + "\nCorrija o arquivo e entregue-o completo de novo."
                                + (" Se o pedido for ambíguo, pergunte ao usuário." if can_ask else "")}]
    return {"divergencias": divergences, "divergencias_codigo": by_segment, "alertas": state["alertas"] + alerts,
            "conferencias": count,
            "mensagens": messages}


def after_conference(state: State) -> str:
    back = state["divergencias"] and state["conferencias"] == 1 and state["entregas"] < MAX_DELIVERIES
    return "agente" if back else "responder"


def shown_notes(notes: str) -> str:
    """As notas que o usuário vê: sem o que o LLM pensou antes da 1ª seção; o que ficou de fora do GoBR sempre aparece."""
    if len(notes) <= NOTES_CHARS:
        return notes
    lines = notes.splitlines()
    start = next((n for n, line in enumerate(lines) if NOTES_HEADER.match(fold(line))), 0)
    shown = memory.short("\n".join(lines[start:]), NOTES_CHARS)
    hidden = [line for line in lines if memory.LEFT_OUT.search(fold(line)) and line not in shown]
    return "\n".join([shown] + hidden)


def apply_p10(state: State) -> State:
    """Se o agente manteve uma frequência que ninguém deu, o código tira a regra (premissa P10)."""
    if state["erros"] or not state["gobr"]:
        return {}
    names = invented_frequencies(state["gobr"], state["segmentos"], _answers_text(state))
    left = drop_rules(state["gobr"], names)
    errors = check(left, memory.binding_text(state["descricao"]), state["notas"], _left_out_before(state),
                   declared_only=_base(state) is not None)[0] if names else ["nada a tirar"]
    if errors:
        return {}

    def keep(divergence: str) -> str | None:
        if any(divergence == p10_divergence(n) for n in names):
            return None
        about = any(divergence.startswith(f'"{n}"') for n in names)
        return f"(sobre a regra que tirei) {divergence}" if about else divergence

    return {"gobr": left, "alertas": state["alertas"] + [
                f'Tirei a regra "{n}": o pedido manda agendar e não dá frequência. Pela premissa P10, sem um bloqueio, esses '
                "clientes seguem a regra da faixa deles. Se quiser uma frequência própria, diga qual." for n in names],
            **{key: [k for d in state[key] if (k := keep(d))] for key in ("divergencias", "divergencias_codigo")}}


def p10_divergence(name: str) -> str:
    return (f'"{name}": o pedido manda agendar e não dá frequência. Pela premissa P10, tire esta regra: sem um bloqueio, '
            "esses clientes seguem a regra da faixa deles.")


def team_alert(state: State) -> list[str]:
    """O time que o arquivo usa, quando o usuário não disse qual."""
    if not state["gobr"] or not _team_is_open(state):
        return []
    teams = "; ".join(f'"{t["nome"]}": {t["definicao"]}' for t in _package(state["gobr"])[1]["times"])
    return [f"O pedido não diz o time (premissa P11). O arquivo usa {teams}."]


def respond(state: State) -> State:
    changed = apply_p10(state)
    state = {**state, **changed}
    changed["alertas"] = state["alertas"] = state["alertas"] + team_alert(state)
    parts = [f"```gobr\n{state['gobr']}\n```"] if state["gobr"] else []
    base, kept = _base(state), memory.current(state)
    if state["mudancas"]:
        parts.append("Mudança no pedido:\n" + "\n".join(f"- {memory.change_text(c)}" for c in state["mudancas"]))
    if state["erros"] and kept:
        parts.append(f"Esta mudança não passou no validador: a versão {kept['n']} e o pedido dela continuam valendo.")
    elif base:
        diff = memory.diff_blocks(_package(base["gobr"])[0].blocks, _package(state["gobr"])[0].blocks)
        parts.append("O que mudou no arquivo:\n" + "\n".join(f"- {d}" for d in diff or ["nada"]))
    if state.get("notas"):
        parts.append(shown_notes(state["notas"]))
    if state["erros"]:
        parts.append(f"Erros que ficaram depois de {state['entregas']} entregas:\n"
                     + "\n".join(f"- {e}" for e in state["erros"]))
    if state["divergencias"]:
        parts.append("Divergências entre o pedido e as regras (conferente):\n"
                     + "\n".join(f"- {d}" for d in state["divergencias"]))
    attention = state["avisos_memoria"] + state["avisos"] + state["alertas"]
    if attention:
        parts.append("Pontos de atenção na modelagem:\n" + "\n".join(f"- {a}" for a in attention))
    if _answers(state):
        parts.append("Perguntas feitas:\n" + "\n".join(f"- {q} -> {a}" for q, a in _answers(state)))
    return {**changed, "resposta": "\n\n".join(parts)}


def explain(res: Resources, state: State) -> State:
    """Responde a uma dúvida com o que o pacote e a memória dizem; o arquivo não muda."""
    now, question, request = memory.current(state), state["mensagem"], "\n".join(state["pedido"])
    sections = find_sections(res, question, res.embedder.queries([question])[0])
    table, alerts = "(ainda não há arquivo)", []
    if now:
        table = rule_table(now["gobr"])
        _, alerts = check(now["gobr"], memory.binding_text(request), left_out_before=frozenset(now["fora"]))
    content = (f"<pedido>\n{request}\n</pedido>\n<regras>\n{table}\n</regras>\n"
               f"<alertas>\n" + ("\n".join(alerts) or "(nenhum)") + "\n</alertas>\n"
               f"<conversa>\n{memory.history_text(state.get('turnos', []))}\n</conversa>\n"
               f"<versoes>\n{memory.versions_text(state)}\n</versoes>\n"
               f"<manual>\n{sections_text(sections)}\n</manual>\n<pergunta>\n{question}\n</pergunta>")
    reply = res.chat([{"role": "system", "content": EXPLAIN_PROMPT.read_text(encoding="utf-8")},
                      {"role": "user", "content": content}])
    answer = GOBR_BLOCK.sub("", reply["content"]).strip()  # código aqui não passou no validador
    return {"resposta": answer or "Não consegui responder a essa dúvida."}


def undo(state: State) -> State:
    target = _base(state)
    return {"versao_atual": target["n"], "pedido": target["pedido"], "sem_resposta": target["sem_resposta"],
            "resposta": f"```gobr\n{target['gobr']}\n```\n\nVoltei à versão {target['n']}, com o pedido dela:\n"
                        + "\n".join(f"- {line}" for line in target["pedido"])}


def remember(state: State) -> State:
    """Fim do turno: grava a versão (só a que passou no validador), o pedido e o registro do turno."""
    turns = state.get("turnos", [])
    out: State = {}
    if state["tipo"] in ("inicial", "novo", "alterar"):
        out, summary = _remember_delivery(state)
    elif state["tipo"] == "desfazer":
        summary = f"voltou à versão {state['versao_atual']}"
    else:
        summary = memory.short(memory.one_line(state["resposta"]))
    record = {"n": len(turns) + 1, "mensagem": state["mensagem"], "tipo": state["tipo"], "resumo": summary,
              "perguntas": _answers(state), "versao": out.get("versao_atual", 0)}
    return {**out, "turnos": turns + [record]}


def _remember_delivery(state: State) -> tuple[State, str]:
    kept = memory.current(state)
    if state["erros"] and kept:
        return {}, f"a mudança não passou no validador; a versão {kept['n']} continua valendo"
    request = memory.request_lines(state["descricao"]) + [
        memory.answer_line(q, a) for q, a in _answers(state) if a != NO_ANSWER]
    unanswered = [g for g in state["lacunas"] if g in _asked_before(state) or state["pergunta_lacunas"]]
    out: State = {"pedido": request, "sem_resposta": unanswered}
    if state["erros"]:
        return out, f"o arquivo não passou no validador: {memory.short('; '.join(state['erros']))}"
    versions = state.get("versoes", [])
    number = len(versions) + 1
    left_out = requested_numbers(memory.binding_text(state["descricao"])) - _clause_numbers(_package(state["gobr"])[0])
    made = {"n": number, "pai": kept["n"] if kept else 0, "pedido": request, "segmentos": state["segmentos"],
            "gobr": state["gobr"], "notas": state["notas"], "fora": sorted(left_out),
            "sem_resposta": unanswered}
    changes = "; ".join(memory.change_text(c) for c in state["mudancas"]) or "pedido " + memory.short("; ".join(request))
    pending = f"; {len(state['divergencias'])} divergências avisadas" if state["divergencias"] else ""
    return {**out, "versoes": versions + [made], "versao_atual": number}, f"versão {number}: {changes}{pending}"


def build_graph(res: Resources, checkpointer=None):
    """`checkpointer` guarda a memória entre turnos; sem ele, ela dura o processo (testes e avaliações)."""
    graph = StateGraph(State)
    graph.add_node("receber", receive)
    graph.add_node("interpretar", lambda s: interpret_message(res, s))
    graph.add_node("explicar", lambda s: explain(res, s))
    graph.add_node("desfazer", undo)
    graph.add_node("lembrar", remember)
    graph.add_node("triagem", lambda s: triage(res, s))
    graph.add_node("perguntar_lacunas", ask_gaps)
    graph.add_node("preparar", lambda s: prepare(res, s))
    graph.add_node("agente", lambda s: act(res, s))
    graph.add_node("ferramentas", lambda s: use_tools(res, s))
    graph.add_node("perguntar", ask)
    graph.add_node("validar", validate)
    graph.add_node("conferir", lambda s: conference(res, s))
    graph.add_node("responder", respond)
    graph.add_edge(START, "receber")
    graph.add_conditional_edges("receber", after_receive, ["triagem", "interpretar"])
    graph.add_conditional_edges("interpretar", after_interpret, ["triagem", "explicar", "desfazer", "lembrar"])
    graph.add_conditional_edges("triagem", after_triage, ["perguntar_lacunas", "preparar"])
    graph.add_conditional_edges("perguntar_lacunas", after_ask_gaps, ["triagem", "preparar"])
    graph.add_edge("preparar", "agente")
    graph.add_conditional_edges("agente", after_act, ["ferramentas", "validar"])
    graph.add_conditional_edges("ferramentas", after_tools, ["perguntar", "agente"])
    graph.add_edge("perguntar", "agente")
    graph.add_conditional_edges("validar", after_validate, ["conferir", "agente", "responder"])
    graph.add_conditional_edges("conferir", after_conference, ["agente", "responder"])
    for last in ("responder", "explicar", "desfazer"):
        graph.add_edge(last, "lembrar")
    graph.add_edge("lembrar", END)
    return graph.compile(checkpointer=InMemorySaver() if checkpointer is None else checkpointer)


@contextmanager
def open_memory(path: Path) -> Iterator[SqliteSaver]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with SqliteSaver.from_conn_string(str(path)) as saver:
        saver.setup()
        yield saver


def conversations(saver: SqliteSaver) -> list[dict]:
    """Conversas guardadas: nome, turnos, versão atual e a 1ª mensagem."""
    with saver.cursor(transaction=False) as cursor:
        names = [row[0] for row in cursor.execute("SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id")]
    found = []
    for name in names:
        state = saver.get_tuple(thread_config(name)).checkpoint["channel_values"]
        turns = state.get("turnos", [])
        found.append({"nome": name, "turnos": len(turns), "versao": state.get("versao_atual", 0),
                      "inicio": turns[0]["mensagem"] if turns else state.get("mensagem", "")})
    return found


def thread_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}, "recursion_limit": 80}


def converse(graph, state: State | None, answer: Callable[[str], str], thread_id: str | None = None) -> State | None:
    """Roda um turno até o fim; cada pergunta do agente vai a `answer`, e a resposta retoma o grafo.

    Sem `thread_id`, a conversa é nova. Com `state=None`, retoma o turno que ficou pela metade (pergunta sem
    resposta ou erro no meio); devolve None se não há nada pendente.
    """
    config = thread_config(thread_id or uuid.uuid4().hex)
    if state is None:
        snapshot = graph.get_state(config)
        if not snapshot.next:
            return None
        out = {"__interrupt__": snapshot.interrupts} if snapshot.interrupts else graph.invoke(None, config)
    else:
        out = graph.invoke(state, config)
    while out.get("__interrupt__"):
        out = graph.invoke(Command(resume=answer(out["__interrupt__"][0].value["pergunta"])), config)
    return out
