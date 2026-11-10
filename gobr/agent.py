"""Fluxo básico do agente (LangGraph): busca exemplos e manual, redige o .gobr com o LLM e valida.

    buscar -> redigir -> validar --(erro e tentativas < MAX_ATTEMPTS)--> redigir
                                 \\-> responder

O LLM só redige (CASCADE-FIRST): quem diz se o .gobr está certo é o parser, e os pontos falhos da
modelagem comercial são os alertas da cascata de `gobr.context`. `chat` recebe as mensagens no formato da
API OpenAI e devolve o texto; `openai_chat` liga ao llama-server, e os testes passam um LLM falso.
"""
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypedDict

from langgraph.graph import END, START, StateGraph

from gobr import index, manual_search
from gobr.context import build
from gobr.parser import parse_file, read_source, unrecognized

MAX_ATTEMPTS = 2
EXAMPLES_K = 3
MANUAL_K = 3
ROOT = Path(__file__).resolve().parent.parent  # os caminhos do manifesto do índice são relativos à raiz
PROMPT = ROOT / "redator" / "prompt_agente.md"
GOBR_BLOCK = re.compile(r"```[ \t]*(?:gobr)?[ \t]*\r?\n(.*?)```", re.DOTALL | re.IGNORECASE)
RULE_LABEL = re.compile(r"\bregra\s+\d+", re.IGNORECASE)  # "Regra 01:" numera o pedido, não é um limite

Chat = Callable[[list[dict]], str]


class State(TypedDict, total=False):
    descricao: str
    excluir: list[str]  # arquivos (e os de mesma assinatura) fora da busca, para avaliar sem o gabarito
    exemplos: list[dict]
    manual: list[dict]
    gobr: str
    notas: str  # o que o LLM escreveu fora do bloco: o que ficou de fora e dúvidas para o usuário
    erros: list[str]
    alertas: list[str]
    tentativas: int
    resposta: str


@dataclass
class Resources:
    examples: index.Index
    manual: manual_search.ManualIndex
    embedder: object  # documents/queries, como `index.Embedder`
    chat: Chat
    whole_manual: bool = False  # manda o manual inteiro no prompt em vez das seções recuperadas


def openai_chat(base_url: str) -> Chat:
    """LLM por uma API compatível com a da OpenAI (llama-server), determinístico e sem raciocínio."""
    from openai import OpenAI  # import tardio: os testes não precisam do cliente

    client = OpenAI(base_url=base_url, api_key="sem-chave")

    def chat(messages: list[dict]) -> str:
        reply = client.chat.completions.create(model="local", messages=messages, temperature=0, seed=0,
                                               max_tokens=3072, reasoning_effort="none")
        choice = reply.choices[0]
        if choice.finish_reason == "length":
            print("aviso: resposta do LLM cortada no limite de tokens", file=sys.stderr)
        if not choice.message.content:
            print("aviso: o LLM devolveu uma resposta vazia", file=sys.stderr)
        return choice.message.content or ""

    return chat


def excluded_chunks(examples: index.Index, names: list[str]) -> frozenset[int]:
    unknown = [n for n in names if n not in examples.files]
    if unknown:
        raise ValueError(f"arquivos fora do índice, não dá para excluí-los da busca: {', '.join(unknown)}")
    signatures = {examples.files[n]["assinatura"] for n in names}
    return frozenset(i for i, c in enumerate(examples.chunks) if examples.files[c["arquivo"]]["assinatura"] in signatures)


def retrieve(res: Resources, state: State) -> State:
    text = state["descricao"]
    vector = res.embedder.queries([text])[0]
    exclude = excluded_chunks(res.examples, state.get("excluir", []))
    file_text = {c["arquivo"]: c["texto"] for c in res.examples.chunks if c["tipo"] == "arquivo"}
    examples = [
        {"arquivo": hit["arquivo"], "descricao": file_text[hit["arquivo"]],
         "gobr": read_source(ROOT / hit["gobr"]).strip()}
        for hit in index.search(res.examples, vector, index.numbers(text), EXAMPLES_K, exclude=exclude)
        if hit["gobr"]
    ]
    if res.whole_manual:
        sections = list(res.manual.sections.values())
    else:
        sections = manual_search.search(res.manual, text, vector, MANUAL_K)
    return {"exemplos": examples, "manual": [{"secao": s["secao"], "texto": s["texto"]} for s in sections],
            "tentativas": 0}


def messages(state: State) -> list[dict]:
    parts = [f"<pedido>\n{state['descricao']}\n</pedido>", "<exemplos>"]
    parts += [f"<exemplo arquivo=\"{e['arquivo']}\">\nDescrição: {e['descricao']}\n```gobr\n{e['gobr']}\n```\n</exemplo>"
              for e in state["exemplos"]]
    parts += ["</exemplos>", "<manual>"]
    parts += [f"<secao numero=\"{s['secao']}\">\n{s['texto']}\n</secao>" for s in state["manual"]]
    parts.append("</manual>")
    if state.get("erros"):
        parts.append(f"<tentativa_anterior>\n```gobr\n{state.get('gobr', '')}\n```\n</tentativa_anterior>")
        parts.append("<erros>\n" + "\n".join(f"- {e}" for e in state["erros"]) + "\n</erros>")
    return [{"role": "system", "content": PROMPT.read_text(encoding="utf-8")},
            {"role": "user", "content": "\n".join(parts)}]


def draft(res: Resources, state: State) -> State:
    reply = res.chat(messages(state))
    block = GOBR_BLOCK.search(reply)
    notes = (reply[:block.start()] + reply[block.end():]) if block else reply
    return {"gobr": block.group(1).strip() if block else "", "notas": notes.strip(),
            "tentativas": state["tentativas"] + 1}


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
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "rascunho.gobr"
        path.write_bytes(gobr_text.replace("\r\n", "\n").encode("utf-8"))  # \r conta como caractere de controle
        file = parse_file(path)
        package = build(path)
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
    errors, alerts = check(state["gobr"], state["descricao"], state.get("notas", ""))
    return {"erros": errors, "alertas": alerts}


def next_step(state: State) -> str:
    return "redigir" if state["erros"] and state["tentativas"] < MAX_ATTEMPTS else "responder"


def respond(state: State) -> State:
    parts = [f"```gobr\n{state['gobr']}\n```"] if state["gobr"] else []
    if state.get("notas"):
        parts.append(state["notas"])
    if state["erros"]:
        parts.append(f"Erros que ficaram depois de {state['tentativas']} tentativas:\n"
                     + "\n".join(f"- {e}" for e in state["erros"]))
    if state["alertas"]:
        parts.append("Pontos de atenção na modelagem:\n" + "\n".join(f"- {a}" for a in state["alertas"]))
    return {"resposta": "\n\n".join(parts)}


def build_graph(res: Resources):
    graph = StateGraph(State)
    graph.add_node("buscar", lambda s: retrieve(res, s))
    graph.add_node("redigir", lambda s: draft(res, s))
    graph.add_node("validar", validate)
    graph.add_node("responder", respond)
    graph.add_edge(START, "buscar")
    graph.add_edge("buscar", "redigir")
    graph.add_edge("redigir", "validar")
    graph.add_conditional_edges("validar", next_step, ["redigir", "responder"])
    graph.add_edge("responder", END)
    return graph.compile()
