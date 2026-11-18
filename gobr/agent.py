"""Fluxo agêntico (LangGraph): o LLM decide buscas e perguntas; o grafo valida e confere toda entrega.

    triagem --lacunas--> perguntar_lacunas --resposta--> triagem
           \\--> preparar -> agente --tool_calls--> ferramentas --(pergunta)--> perguntar --> agente
                                     \\--texto--> validar --erro--> agente
                                                         \\--ok--> conferir --divergência na 1ª--> agente
                                                                            \\--> responder

O LLM só extrai, redige e escolhe ferramentas (CASCADE-FIRST): a triagem devolve os segmentos do pedido em
JSON e o código decide o que falta perguntar; quem diz se o .gobr está certo é o parser, e o que cada regra
faz vem do pacote de `gobr.context`. Na conferência, o código compara ação e frequência com os segmentos, e
o conferente (LLM) compara, em português, a tabela do pacote com o pedido. `chat` recebe mensagens no formato da API OpenAI e devolve a mensagem do assistente;
`openai_chat` liga ao llama-server, e os testes passam um LLM falso. Perguntas ao usuário pausam o grafo
com `interrupt()`; `converse` retoma com a resposta.
"""
import json
import re
import sys
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from gobr import index, manual_search
from gobr.context import build
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
ACTIONS = ("agendar", "nao_agendar", "indefinido")
RESIDUAL = re.compile(r"\b(demais|restantes?)\b")  # no nome do segmento: "os demais" não precisa de critério
GOBR_BLOCK = re.compile(r"```[ \t]*(?:gobr)?[ \t]*\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)
RULE_LABEL = re.compile(r"\bregra\s+\d+", re.IGNORECASE)  # "Regra 01:" numera o pedido, não é um limite
ASK = "perguntar_usuario"
NO_ANSWER = "Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi."
QUESTION_LIMIT = "Limite de perguntas atingido: siga com a premissa mais provável e diga nas notas qual foi."
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

Chat = Callable[..., dict]  # chat(messages, tools=None, schema=None) -> mensagem do assistente


class State(TypedDict, total=False):
    descricao: str
    excluir: list[str]  # arquivos (e os de mesma assinatura) fora da busca, para avaliar sem o gabarito
    exemplos: list[dict]  # busca inicial
    segmentos: list[dict]  # o pedido, segmento a segmento, segundo a triagem
    lacunas: list[str]  # o que falta nos segmentos (o código decide, não o LLM)
    lacunas_iniciais: list[str]
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
    resposta: str


@dataclass
class Resources:
    examples: index.Index
    manual: manual_search.ManualIndex
    embedder: object  # documents/queries, como `index.Embedder`
    chat: Chat
    whole_manual: bool = False  # manda o manual inteiro na 1ª mensagem em vez das seções recuperadas


def openai_chat(base_url: str) -> Chat:
    """LLM por uma API compatível com a da OpenAI (llama-server), determinístico e sem raciocínio."""
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
    found = gaps(segments)
    return {"segmentos": segments, "lacunas": found, "lacunas_iniciais": state.get("lacunas_iniciais", found),
            "avisos": warnings}


def after_triage(state: State) -> str:
    return "perguntar_lacunas" if state["lacunas"] and not state.get("pergunta_lacunas") else "preparar"


def ask_gaps(state: State) -> State:
    """Uma só pergunta, montada pelo código, com todas as lacunas; a resposta volta para a triagem."""
    question = ("Para escrever as regras sem chutar, faltam estes dados no pedido:\n"
                + "\n".join(f"- {g}" for g in state["lacunas"]) + "\nResponda numa mensagem só.")
    answer = str(interrupt({"pergunta": question})).strip()
    return {"pergunta_lacunas": question, "resposta_lacunas": answer or NO_ANSWER}


def after_ask_gaps(state: State) -> str:
    return "preparar" if state["resposta_lacunas"] == NO_ANSWER else "triagem"


def segments_text(segments: list[dict]) -> str:
    def action(s: dict) -> str:
        if s["acao"] == "nao_agendar":
            return "não agendar"
        if s["acao"] == "agendar":
            return f"agendar a cada {s['frequencia_dias']} dias" if s["frequencia_dias"] else "agendar (frequência não dada)"
        return "indefinida"
    return "\n".join(f'- "{s["segmento"]}" | critério: {s["criterio"] or "(não dado)"} | ação: {action(s)}'
                     for s in segments)


def prepare(res: Resources, state: State) -> State:
    text = state["descricao"]
    vector = res.embedder.queries([text])[0]
    examples = find_examples(res, text, vector, state.get("excluir", []))
    if res.whole_manual:
        sections = [{"secao": s["secao"], "texto": s["texto"]} for s in res.manual.sections.values()]
    else:
        sections = find_sections(res, text, vector)
    first = f"<pedido>\n{text}\n</pedido>\n"
    if state.get("segmentos"):
        answered = f"\nO usuário respondeu: {state['resposta_lacunas']}" if state.get("resposta_lacunas") else ""
        first += (f"<segmentos>\nO pedido, segmento a segmento (com as respostas do usuário, se houve pergunta). "
                  f"Escreva uma regra por segmento, com o nome do segmento e estes valores.{answered}\n"
                  f"{segments_text(state['segmentos'])}\n</segmentos>\n")
    first += (f"<exemplos>\n{examples_text(examples)}\n</exemplos>\n"
              f"<manual>\n{sections_text(sections)}\n</manual>")
    unresolved = ("Lacuna do pedido sem resposta do usuário" if state.get("resposta_lacunas", NO_ANSWER) == NO_ANSWER
                  else "Lacuna que a resposta do usuário não resolveu")
    warnings = state.get("avisos", []) + [f"{unresolved}: {g}" for g in state.get("lacunas", [])]
    return {"exemplos": examples, "perguntas": [], "passos": 0, "entregas": 0, "conferencias": 0, "avisos": warnings,
            "divergencias": [], "divergencias_codigo": [], "valido": None, "restaurada": False,
            "mensagens": [{"role": "system", "content": PROMPT.read_text(encoding="utf-8")},
                          {"role": "user", "content": first}]}


def act(res: Resources, state: State) -> State:
    messages, steps = state["mensagens"], state["passos"] + 1
    if steps == MAX_STEPS:
        messages = messages + [{"role": "user", "content": LAST_STEP}]
    reply = res.chat(messages, tools=TOOLS if steps < MAX_STEPS else None)
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


def requested_numbers(text: str) -> set[int]:
    """Inteiros do pedido que o .gobr tem de ter: sem o 0, sem "Regra NN" e com 1.500,00 lido como 1500."""
    text = RULE_LABEL.sub(" ", text)
    text = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", text)
    text = re.sub(r"(?<=\d),\d+", "", text)
    return set(index.numbers(text)) - {0}


def check(gobr_text: str, description: str, notes: str = "") -> tuple[list[str], list[str]]:
    """Erros (o .gobr não serve e volta ao LLM) e alertas da cascata (pontos falhos para o usuário).

    Um número do pedido conta quando aparece numa cláusula (não no nome da regra) ou quando o LLM diz, nas
    notas, que o deixou de fora porque o GoBR não o expressa.
    """
    if not gobr_text:
        return ["A resposta não trouxe um bloco ```gobr com o arquivo."], []
    file, package = _package(gobr_text)
    errors = [f"{block_id}: trecho não reconhecido: {getattr(item, 'text', item)}" for block_id, item in unrecognized(file)]
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
    in_clauses = {n for b in file.blocks for c in b.all_clauses() for n in index.numbers(c.text)}
    absent = requested_numbers(description) - in_clauses
    left_out = sorted(absent & index.numbers(notes))
    missing = sorted(absent - index.numbers(notes))
    if missing:
        errors.append(f"Números do pedido ausentes nas cláusulas do GoBR: {', '.join(map(str, missing))}. Ponha cada "
                      "um numa cláusula ou, se o GoBR não o expressa, diga depois do código o que ficou de fora, "
                      "com o número.")
    alerts = package["alertas"] + [f"{r['nome']}: {a}" for r in package["regras"] for a in r["alertas"]]
    if left_out:
        alerts.append(f"Números do pedido que ficaram de fora do GoBR (ver notas): {', '.join(map(str, left_out))}.")
    return errors, alerts


def validate(state: State) -> State:
    reply = state["mensagens"][-1]["content"]
    block = GOBR_BLOCK.search(reply)
    gobr = strip_comments(block.group(1).strip()) if block else ""
    notes = ((reply[:block.start()] + reply[block.end():]) if block else reply).strip()
    errors, alerts = check(gobr, state["descricao"], notes)
    deliveries = state["entregas"] + 1
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
    named = sorted(((fold(s["segmento"]), s) for s in segments), key=lambda pair: -len(pair[0]))
    found = []
    for rule in package["regras"]:
        name = fold(rule["nome"])
        seg = next((s for key, s in named
                    if name == key or name.startswith(key + ":")), None)  # "Ativos: compra ..." é o segmento Ativos
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


def _short(text: str, limit: int = 300) -> str:
    """O conferente às vezes pensa alto dentro do campo `motivo`; na resposta, só cabe o começo."""
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def confer(chat: Chat, gobr_text: str, description: str, notes: str = "") -> tuple[list[str], list[str]]:
    """Divergências entre o pedido e o que as regras fazem, e alertas do próprio conferente."""
    content = (f"<pedido>\n{description}\n</pedido>\n<regras>\n{rule_table(gobr_text)}\n</regras>\n"
               f"<notas_do_redator>\n{notes or '(nenhuma)'}\n</notas_do_redator>")
    reply = chat([{"role": "system", "content": CONFERENCE_PROMPT.read_text(encoding="utf-8")},
                  {"role": "user", "content": content}], schema=CONFERENCE_SCHEMA)
    try:
        data = json.loads(reply["content"])
        divergences = [f'"{r["regra"]}": {_short(r["motivo"])} (pedido: "{_short(r["trecho_do_pedido"])}")'
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


def respond(state: State) -> State:
    parts = [f"```gobr\n{state['gobr']}\n```"] if state["gobr"] else []
    if state.get("notas"):
        parts.append(state["notas"])
    if state["erros"]:
        parts.append(f"Erros que ficaram depois de {state['entregas']} entregas:\n"
                     + "\n".join(f"- {e}" for e in state["erros"]))
    if state["divergencias"]:
        parts.append("Divergências entre o pedido e as regras (conferente):\n"
                     + "\n".join(f"- {d}" for d in state["divergencias"]))
    attention = state.get("avisos", []) + state["alertas"]
    if attention:
        parts.append("Pontos de atenção na modelagem:\n" + "\n".join(f"- {a}" for a in attention))
    if _answers(state):
        parts.append("Perguntas feitas:\n" + "\n".join(f"- {q} -> {a}" for q, a in _answers(state)))
    return {"resposta": "\n\n".join(parts)}


def build_graph(res: Resources):
    graph = StateGraph(State)
    graph.add_node("triagem", lambda s: triage(res, s))
    graph.add_node("perguntar_lacunas", ask_gaps)
    graph.add_node("preparar", lambda s: prepare(res, s))
    graph.add_node("agente", lambda s: act(res, s))
    graph.add_node("ferramentas", lambda s: use_tools(res, s))
    graph.add_node("perguntar", ask)
    graph.add_node("validar", validate)
    graph.add_node("conferir", lambda s: conference(res, s))
    graph.add_node("responder", respond)
    graph.add_edge(START, "triagem")
    graph.add_conditional_edges("triagem", after_triage, ["perguntar_lacunas", "preparar"])
    graph.add_conditional_edges("perguntar_lacunas", after_ask_gaps, ["triagem", "preparar"])
    graph.add_edge("preparar", "agente")
    graph.add_conditional_edges("agente", after_act, ["ferramentas", "validar"])
    graph.add_conditional_edges("ferramentas", after_tools, ["perguntar", "agente"])
    graph.add_edge("perguntar", "agente")
    graph.add_conditional_edges("validar", after_validate, ["conferir", "agente", "responder"])
    graph.add_conditional_edges("conferir", after_conference, ["agente", "responder"])
    graph.add_edge("responder", END)
    return graph.compile(checkpointer=InMemorySaver())


def converse(graph, state: State, answer: Callable[[str], str]) -> State:
    """Roda o grafo até o fim; cada pergunta do agente vai a `answer`, e a resposta retoma o grafo."""
    config = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 80}
    out = graph.invoke(state, config)
    while out.get("__interrupt__"):
        out = graph.invoke(Command(resume=answer(out["__interrupt__"][0].value["pergunta"])), config)
    return out
