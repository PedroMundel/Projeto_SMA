"""Cossenos entre embeddings: o gerado com o gabarito, com o manual e entre as respostas do mesmo pedido.

São medidas de semelhança de texto, complementares à `outcomes`, e não medem significado: trocar 30 por 60 dias quase não
muda o vetor. Por isso vêm com uma referência: o piso (os gabaritos dos OUTROS arquivos) ou o mesmo cálculo no gabarito.
Para "a cláusula existe no manual?", a checagem exata é a do catálogo (`reconhecidas`), não o cosseno.
Arquivo que não existe ou está vazio vale 0.
"""
import numpy as np

from gobr.ir import GobrFile
from gobr.parser import unrecognized
from gobr.text import strip_comment


def _unit(vectors) -> np.ndarray:
    """Vetores de norma 1 em float64: em meia precisão, o cosseno passava de 1."""
    vectors = np.asarray(vectors, dtype=np.float64)
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def code_text(source: str) -> str:
    """O arquivo sem comentários nem linhas vazias: os do professor têm links e títulos que o agente não escreve."""
    lines = (strip_comment(line).rstrip() for line in source.splitlines())
    return "\n".join(line for line in lines if line.strip())


def cosine_rows(made: dict[str, str], gold: dict[str, str], embedder) -> list[dict]:
    """Uma linha por gabarito: `cosseno`, `piso` (None se só há um gabarito) e `mais_proximo`."""
    names = list(gold)
    present = [n for n in names if code_text(made.get(n, ""))]
    texts = [code_text(made[n]) for n in present] + [code_text(gold[n]) for n in names]
    vectors = _unit(embedder.documents(texts)) if present else np.zeros((0, 1))
    similarities = vectors[:len(present)] @ vectors[len(present):].T if present else vectors
    rows = []
    for name in names:
        if name not in present:
            rows.append({"nome": name, "cosseno": 0.0, "piso": None, "mais_proximo": False})
            continue
        own = names.index(name)
        line = similarities[present.index(name)]
        others = np.delete(line, own)
        rows.append({"nome": name, "cosseno": float(line[own]), "piso": float(others.mean()) if len(others) else None,
                     "mais_proximo": bool(line[own] > others.max()) if len(others) else None})
    return rows


def rule_clauses(file: GobrFile) -> list[str]:
    """Filtros, recortes de data e ações das regras de parâmetros, sem repetir; os trechos que o parser não leu contam."""
    texts = [c.text for b in file.of_kind("parametros") for c in b.temporal + b.filters + b.actions]
    texts += [s for b in file.of_kind("parametros") for s in b.unclassified]
    return list(dict.fromkeys(texts))


def manual_rows(files: dict[str, GobrFile], manual_vectors: np.ndarray, embedder) -> list[dict]:
    """Por arquivo: cosseno médio de cada cláusula com o trecho mais próximo do manual, e a fração que o catálogo reconhece."""
    clauses = {name: rule_clauses(file) for name, file in files.items()}
    texts = list(dict.fromkeys(t for found in clauses.values() for t in found))
    best = {}
    if texts:
        scores = _unit(embedder.queries(texts)) @ _unit(manual_vectors).T
        best = dict(zip(texts, scores.max(axis=1)))
    rows = []
    for name, file in files.items():
        own = clauses[name]
        unknown = {getattr(item, "text", item) for _, item in unrecognized(file)}
        rows.append({"nome": name, "clausulas": len(own), "cosseno": float(np.mean([best[t] for t in own])) if own else 0.0,
                     "reconhecidas": sum(t not in unknown for t in own) / len(own) if own else 0.0})
    return rows


def deliveries(messages: list[dict], block_pattern) -> list[str]:
    """As entregas do LLM numa conversa: o bloco gobr de cada resposta que trouxe um."""
    found = []
    for message in messages:
        if message["role"] == "assistant" and (match := block_pattern.search(message.get("content") or "")):
            found.append(code_text(match.group(1)))
    return [text for text in found if text]


def between_responses(responses: list[str], embedder) -> dict | None:
    """Cosseno entre respostas do mesmo pedido; None se há menos de duas. `seguidas`: cada uma com a anterior."""
    if len(responses) < 2:
        return None
    vectors = _unit(embedder.documents(responses))
    consecutive = [float(a @ b) for a, b in zip(vectors, vectors[1:])]
    return {"respostas": len(responses), "seguidas": consecutive, "primeira_ultima": float(vectors[0] @ vectors[-1]),
            "iguais": len(set(responses)) == 1}
