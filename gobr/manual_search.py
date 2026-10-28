"""Busca no manual GoBR: embeddings, BM25 e a fusão dos dois por posição (RRF), devolvendo seções.

Os chunks vêm de `data/manual/` (`python -m gobr manual`). A nota de uma seção é a do seu melhor chunk; o
agente recebe o texto inteiro da seção, não o chunk ("pequeno para achar, grande para dar contexto").
"""
import hashlib
import json
import math
import os
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np

MODES = ("denso", "bm25", "hibrido")
DEFAULT_MODE = "hibrido"
RRF_K = 60  # constante usual da fusão por posição (Cormack et al., 2009)


def tokens(text: str) -> list[str]:
    plain = unicodedata.normalize("NFKD", text.lower())
    return re.findall(r"\w+", "".join(c for c in plain if not unicodedata.combining(c)))


class BM25:
    def __init__(self, documents: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.freqs = [Counter(d) for d in documents]
        self.lengths = np.array([len(d) for d in documents], dtype=np.float32)
        self.average = float(self.lengths.mean()) if documents else 0.0
        df = Counter(t for d in self.freqs for t in d)
        n = len(documents)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: list[str]) -> np.ndarray:
        out = np.zeros(len(self.freqs), dtype=np.float32)
        norm = self.k1 * (1 - self.b + self.b * self.lengths / self.average)
        for term in set(query) & self.idf.keys():
            tf = np.array([f[term] for f in self.freqs], dtype=np.float32)
            out += self.idf[term] * tf * (self.k1 + 1) / (tf + norm)
        return out


@dataclass
class ManualIndex:
    model: str
    chunks: list[dict]
    vectors: np.ndarray
    sections: dict[str, dict]
    bm25: BM25


def _read_manual(manual_dir: Path) -> tuple[list[dict], dict[str, dict], str]:
    raw_chunks = (manual_dir / "chunks.jsonl").read_text(encoding="utf-8")
    raw_sections = (manual_dir / "secoes.json").read_text(encoding="utf-8")
    sections = {s["secao"]: s for s in json.loads(raw_sections)}
    digest = hashlib.sha256((raw_chunks + raw_sections).encode()).hexdigest()[:12]
    return [json.loads(line) for line in raw_chunks.splitlines()], sections, digest


def build(manual_dir: Path, embedder) -> tuple[ManualIndex, dict]:
    chunks, sections, digest = _read_manual(manual_dir)
    if not chunks:
        raise SystemExit(f"nenhum chunk em {manual_dir}; rode `python -m gobr manual` antes")
    vectors = np.asarray(embedder.documents([c["texto"] for c in chunks]), dtype=np.float32)
    manifest = {"modelo": embedder.model, "manual": manual_dir.resolve().as_posix(), "manual_sha256": digest,
                "n_chunks": len(chunks), "dimensao": int(vectors.shape[1])}
    return ManualIndex(embedder.model, chunks, vectors, sections, BM25([tokens(c["texto"]) for c in chunks])), manifest


def save(index: ManualIndex, manifest: dict, out_dir: Path) -> None:
    """Grava os vetores; o caminho do manual fica relativo ao índice, para carregar de qualquer pasta."""
    out_dir.mkdir(parents=True, exist_ok=True)
    np.save(out_dir / "vetores.npy", index.vectors.astype(np.float16))
    manual = Path(os.path.relpath(manifest["manual"], out_dir.resolve())).as_posix()
    (out_dir / "manifesto.json").write_text(json.dumps({**manifest, "manual": manual}, ensure_ascii=False, indent=1),
                                            encoding="utf-8")


def load(index_dir: Path) -> ManualIndex:
    manifest = json.loads((index_dir / "manifesto.json").read_text(encoding="utf-8"))
    manual_dir = index_dir / manifest["manual"]
    chunks, sections, digest = _read_manual(manual_dir)
    if digest != manifest["manual_sha256"]:
        raise SystemExit(f"{manual_dir} mudou desde a indexação; rode `indexar-manual` de novo")
    vectors = np.load(index_dir / "vetores.npy").astype(np.float32)
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)  # o float16 em disco tira a norma de 1
    return ManualIndex(manifest["modelo"], chunks, vectors, sections, BM25([tokens(c["texto"]) for c in chunks]))


def _ranks(scores: np.ndarray) -> np.ndarray:
    """Posição 1 = maior nota; notas iguais dividem a mesma posição (1 + quantas notas são maiores)."""
    ascending = np.sort(scores)
    return (1 + len(scores) - np.searchsorted(ascending, scores, side="right")).astype(np.float32)


def chunk_scores(index: ManualIndex, text: str, vector: np.ndarray, mode: str) -> np.ndarray:
    if mode not in MODES:
        raise ValueError(f"modo desconhecido: {mode}; use {MODES}")
    def dense():
        return index.vectors @ np.asarray(vector, dtype=np.float32)

    def lexical():
        return index.bm25.scores(tokens(text))

    if mode == "denso":
        return dense()
    if mode == "bm25":
        return lexical()
    bm25 = lexical()
    return 1 / (RRF_K + _ranks(dense())) + np.where(bm25 > 0, 1 / (RRF_K + _ranks(bm25)), 0)  # sem termo em comum, 0


def search(index: ManualIndex, text: str, vector: np.ndarray, k: int = 3, mode: str = DEFAULT_MODE) -> list[dict]:
    """Top-k seções pela nota do melhor chunk; cada uma traz o chunk que a achou e o texto completo."""
    scores = chunk_scores(index, text, vector, mode)
    hits: dict[str, dict] = {}
    for i in map(int, np.argsort(-scores, kind="stable")):
        number = index.chunks[i]["secao"]
        if number not in hits:
            section = index.sections[number]
            hits[number] = {"secao": number, "titulo": section["titulo"], "pagina": section["pagina"],
                            "nota": round(float(scores[i]), 4), "chunk": index.chunks[i], "texto": section["texto"]}
            if len(hits) == k:
                break
    return list(hits.values())


def evaluate(index: ManualIndex, embedder, queries: list[dict], k: int = 5) -> dict:
    """Recall@1/@k e MRR por modo e por tipo de consulta; acerto = uma das seções `esperadas`."""
    if not queries:
        raise SystemExit("nenhuma consulta para avaliar")
    unknown = sorted({s for q in queries for s in q["esperadas"]} - {c["secao"] for c in index.chunks})
    if unknown:
        raise SystemExit(f"seções esperadas sem nenhum chunk no manual: {', '.join(unknown)}")
    vectors = embedder.queries([q["consulta"] for q in queries])
    table = {}
    for mode in MODES:
        ranks = []
        for query, vector in zip(queries, vectors):
            found = [h["secao"] for h in search(index, query["consulta"], vector, k, mode)]
            ranks.append(next((n for n, s in enumerate(found, 1) if s in query["esperadas"]), None))
        for kind in ["todas", *sorted({q["tipo"] for q in queries})]:
            chosen = [r for r, q in zip(ranks, queries) if kind in ("todas", q["tipo"])]
            table[(mode, kind)] = {
                "n": len(chosen),
                "recall@1": sum(r == 1 for r in chosen) / len(chosen),
                f"recall@{k}": sum(r is not None for r in chosen) / len(chosen),
                "mrr": sum(1 / r for r in chosen if r) / len(chosen),
            }
    return table
