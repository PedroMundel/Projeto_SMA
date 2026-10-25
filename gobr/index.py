"""Índice de embeddings das descrições, para o RAG recuperar regras parecidas com o pedido do usuário.

Três tipos de chunk por arquivo: o arquivo inteiro (resumo + uma linha por regra), cada regra (com a 1ª
frase do resumo como contexto) e cada consulta hipotética. A busca usa por padrão só o vetor de arquivo,
reordenado pelos números em comum; a regra mais parecida do arquivo volta junto. Os outros tipos ficam no
índice para a ablação de `evaluate`. Arquivos com a mesma assinatura estrutural contam como um só resultado.

O texto embutido vem da descrição, nunca do DSL, e não leva o nome literal da regra (que carrega empresa
e boilerplate); o nome e o caminho do .gobr ficam no metadado, para o agente mostrar o código de exemplo.
"""
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

KINDS = ("arquivo", "regra", "consulta")
VARIANTS = {"arquivo": ("arquivo",), "arquivo+regra": ("arquivo", "regra"), "multi-vetor": KINDS}
DEFAULT_KINDS = VARIANTS["arquivo"]  # o multi-vetor perdeu na avaliação (docs/relatorio_indexacao.md)
NUMBER_WEIGHT = 0.2
NUMBER = re.compile(r"\d+")
# Modelos sem prompts na config do sentence-transformers precisam do prefixo explícito (consulta, documento).
PREFIXES = {"intfloat/multilingual-e5-small": ("query: ", "passage: ")}


class Embedder:
    def __init__(self, model: str):
        from sentence_transformers import SentenceTransformer  # import tardio: os testes não carregam torch

        self.model = model
        self._st = SentenceTransformer(model)
        self._query_prefix, self._document_prefix = PREFIXES.get(model, (None, None))

    def documents(self, texts: list[str]) -> np.ndarray:
        return self._st.encode_document(texts, prompt=self._document_prefix, normalize_embeddings=True, batch_size=8)

    def queries(self, texts: list[str]) -> np.ndarray:
        return self._st.encode_query(texts, prompt=self._query_prefix, normalize_embeddings=True, batch_size=8)


@dataclass
class Index:
    model: str
    chunks: list[dict]
    vectors: np.ndarray
    files: dict[str, dict]


def rule_line(rule: dict) -> str:
    parts = [f"{rule['segmento']}: {rule['criterio']}", rule["frequencia"], rule["observacao"]]
    return "; ".join(p for p in parts if p)


def chunks(name: str, description: dict) -> list[dict]:
    summary = description["resumo"]
    context = summary.split(". ")[0].rstrip(".")
    lines = [rule_line(r) for r in description["regras"]]
    out = [{"arquivo": name, "tipo": "arquivo", "regra": None, "texto": "\n".join([summary, *lines])}]
    out += [
        {"arquivo": name, "tipo": "regra", "regra": r["id"], "nome": r["nome"], "texto": f"{context}.\n{line}"}
        for r, line in zip(description["regras"], lines)
    ]
    out += [{"arquivo": name, "tipo": "consulta", "regra": None, "texto": q} for q in description["consultas_hipoteticas"]]
    return out


def signature(package: dict) -> str:
    """Hash da estrutura de cada regra, em ordem: tipo, tipo de fonte (time, carteira ou segmentação, sem o
    nome), quando, filtros e ações. Nomes de regra, time e carteira ficam de fora."""
    structure = [
        [r["tipo_bloco"], r["fonte"].split()[1], r["quando_executa"], [f["codigo"] for f in r["filtros"]],
         [a["codigo"] for a in r["acoes"]]]
        for r in package["regras"]
    ]
    return hashlib.sha256(json.dumps(structure, ensure_ascii=False).encode("utf-8")).hexdigest()[:12]


def _first(name: str, directories: list[Path]) -> Path | None:
    return next((d / name for d in directories if (d / name).exists()), None)


def build(descriptions_dir: Path, context_dirs: list[Path], gobr_dirs: list[Path], embedder) -> Index:
    all_chunks, files = [], {}
    for path in sorted(p for p in descriptions_dir.glob("*.json") if not p.name.endswith(".falha.json")):
        package_path = _first(f"{path.stem}.json", context_dirs)
        if package_path is None:
            raise SystemExit(f"{path.stem}: pacote de contexto não encontrado em {context_dirs}")
        gobr_path = _first(f"{path.stem}.gobr", gobr_dirs)
        if gobr_path is None:
            print(f"aviso: {path.stem}.gobr não encontrado em {gobr_dirs}", file=sys.stderr)
        file_chunks = chunks(path.stem, json.loads(path.read_text(encoding="utf-8")))
        files[path.stem] = {
            "assinatura": signature(json.loads(package_path.read_text(encoding="utf-8"))),
            "descricao": path.as_posix(),
            "gobr": gobr_path.as_posix() if gobr_path else None,
            "numeros": sorted(numbers(file_chunks[0]["texto"])),
        }
        all_chunks += file_chunks
    if not files:
        raise SystemExit(f"nenhuma descrição .json em {descriptions_dir}")
    vectors = np.asarray(embedder.documents([c["texto"] for c in all_chunks]), dtype=np.float32)
    return Index(embedder.model, all_chunks, vectors, files)


def save(index: Index, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "vetores.npy", index.vectors.astype(np.float16))
    (out_dir / "chunks.jsonl").write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in index.chunks), encoding="utf-8")
    manifest = {
        "modelo": index.model,
        "dimensao": int(index.vectors.shape[1]),
        "chunks": {kind: sum(c["tipo"] == kind for c in index.chunks) for kind in KINDS},
        "criado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "arquivos": index.files,
    }
    (out_dir / "manifesto.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")


def load(index_dir: Path) -> Index:
    manifest = json.loads((index_dir / "manifesto.json").read_text(encoding="utf-8"))
    lines = (index_dir / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
    vectors = np.load(index_dir / "vetores.npy").astype(np.float32)
    if len(vectors) != len(lines):
        raise SystemExit(f"{index_dir}: {len(lines)} chunks e {len(vectors)} vetores; reconstrua o índice")
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)  # o float16 em disco tira a norma de 1 em até 0,004
    return Index(manifest["modelo"], [json.loads(line) for line in lines], vectors, manifest["arquivos"])


def numbers(text: str) -> frozenset[int]:
    return frozenset(int(n) for n in NUMBER.findall(text))


def search(index: Index, query: np.ndarray, query_numbers=frozenset(), k: int = 5, kinds=DEFAULT_KINDS,
           exclude=frozenset(), weight: float = NUMBER_WEIGHT) -> list[dict]:
    """Top-k arquivos, no máximo um por assinatura; `equivalentes` lista os de mesma estrutura.

    Nota do arquivo = maior cosseno entre os seus chunks dos tipos pedidos + `weight` × Jaccard entre os
    números da consulta e os da descrição. O embedding sozinho não separa 30/45 de 60/90 dias.
    """
    scores = index.vectors @ np.asarray(query, dtype=np.float32)
    names = list(index.files)
    position = {name: n for n, name in enumerate(names)}
    owner = np.array([position[c["arquivo"]] for c in index.chunks])
    kind = np.array([c["tipo"] for c in index.chunks])
    usable = np.isin(kind, kinds)
    usable[list(exclude)] = False
    best = np.full(len(names), -np.inf)
    np.maximum.at(best, owner[usable], scores[usable])
    if weight and query_numbers:
        best += weight * np.array([_jaccard(query_numbers, frozenset(index.files[n]["numeros"])) for n in names])
    groups: dict[str, list[str]] = {}
    for n in np.argsort(-best, kind="stable"):  # empate: ordem alfabética dos arquivos
        if best[n] > -np.inf:
            groups.setdefault(index.files[names[n]]["assinatura"], []).append(names[n])
    hits = []
    for sig, group in list(groups.items())[:k]:
        rules = list(np.flatnonzero((owner == position[group[0]]) & (kind == "regra")))
        hits.append({
            "arquivo": group[0],
            "nota": round(float(best[position[group[0]]]), 4),
            "assinatura": sig,
            "regra_mais_parecida": index.chunks[max(rules, key=lambda i: scores[i])] if rules else None,
            "equivalentes": group[1:],
            "descricao": index.files[group[0]]["descricao"],
            "gobr": index.files[group[0]]["gobr"],
        })
    return hits


def _jaccard(a: frozenset, b: frozenset) -> float:
    return len(a & b) / len(a | b)  # só chamado com `a` não vazio


def _rank(hits: list[dict], expected_signature: str) -> int | None:
    return next((n for n, h in enumerate(hits, 1) if h["assinatura"] == expected_signature), None)


def evaluate(index: Index, embedder, labelled: dict[str, dict[str, str]], k: int = 5) -> dict:
    """Recall@1/@k e MRR por variante de índice (tipos de chunk × reordenação por números) e conjunto.

    `labelled` mapeia o nome do conjunto (ex.: "ouro", "cegas") para {arquivo esperado: consulta}. Acerto é
    devolver um arquivo com a assinatura do esperado. As consultas hipotéticas do próprio índice entram como
    dois conjuntos a mais, tiradas do índice na hora da busca: só a própria ("consulta_propria") ou todas
    as dos arquivos de mesma assinatura ("consulta_estrutura"), já que uma duplicata também conta como acerto.
    """
    unknown = [f"{group}:{name}" for group, queries in labelled.items() for name in queries if name not in index.files]
    if unknown:
        raise SystemExit(f"consultas para arquivos fora do índice: {', '.join(unknown)}")
    cases = {}  # conjunto -> [(assinatura esperada, texto, chunks excluídos)]
    for group, queries in labelled.items():
        cases[group] = [(index.files[name]["assinatura"], text, frozenset()) for name, text in queries.items()]
    hypothetical = [i for i, c in enumerate(index.chunks) if c["tipo"] == "consulta"]
    sig_of = [index.files[index.chunks[i]["arquivo"]]["assinatura"] for i in hypothetical]
    by_signature: dict[str, frozenset[int]] = {}
    for i, sig in zip(hypothetical, sig_of):
        by_signature[sig] = by_signature.get(sig, frozenset()) | {i}
    texts = [index.chunks[i]["texto"] for i in hypothetical]
    cases["consulta_propria"] = [(sig, t, frozenset({i})) for sig, t, i in zip(sig_of, texts, hypothetical)]
    cases["consulta_estrutura"] = [(sig, t, by_signature[sig]) for sig, t in zip(sig_of, texts)]
    cases = {group: items for group, items in cases.items() if items}
    vectors = {group: embedder.queries([text for _, text, _ in items])
               for group, items in cases.items() if group != "consulta_estrutura"}
    if "consulta_propria" in vectors:
        vectors["consulta_estrutura"] = vectors["consulta_propria"]  # mesmos textos
    table = {}
    for variant, kinds in VARIANTS.items():
        for weight in (0.0, NUMBER_WEIGHT):
            for group, items in cases.items():
                if group == "consulta_estrutura" and "consulta" not in kinds:
                    continue  # sem chunks de consulta no índice, é igual a consulta_propria
                ranks = [
                    _rank(search(index, v, numbers(text), k, kinds, ex, weight), sig)
                    for (sig, text, ex), v in zip(items, vectors[group])
                ]
                table[(variant, weight, group)] = {
                    "n": len(ranks),
                    "recall@1": sum(r == 1 for r in ranks) / len(ranks),
                    f"recall@{k}": sum(r is not None for r in ranks) / len(ranks),
                    "mrr": sum(1 / r for r in ranks if r) / len(ranks),
                    "posicoes": ranks if len(ranks) <= 30 else None,
                }
    return table
