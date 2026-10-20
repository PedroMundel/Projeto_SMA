"""Pick, among the redator candidates for one file, the valid answer that agrees most with the others.

Agreement is the mean text similarity per rule (segment, criterion, frequency, observation) plus
the summary: the medoid of the candidate set. Low agreement marks files worth a human look.
"""
import hashlib
import json
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

from gobr.validate import Report, check


@dataclass
class Candidate:
    path: Path
    answer: dict | None
    report: Report


def load(path: Path, package: dict) -> Candidate:
    try:
        answer = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        return Candidate(path, None, Report(errors=[f"JSON inválido em {path.name}: {error}"]))
    return Candidate(path, answer, check(answer, package))


def similarity(a: dict, b: dict) -> float:
    pairs = [(a["resumo"], b["resumo"])]
    pairs += [(_rule_text(x), _rule_text(y)) for x, y in zip(a["regras"], b["regras"])]
    return sum(SequenceMatcher(None, _normalized(x), _normalized(y)).ratio() for x, y in pairs) / len(pairs)


def _rule_text(rule: dict) -> str:
    return " | ".join(rule[k] for k in ("segmento", "criterio", "frequencia", "observacao"))


def _normalized(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def choose(candidates: list[Candidate]) -> tuple[Candidate | None, float | None]:
    """Medoid of the valid candidates and the mean pairwise agreement among them
    (None when fewer than two are valid: there is nothing to agree with)."""
    valid = [c for c in candidates if c.report.ok]
    if not valid:
        return None, None
    if len(valid) == 1:
        return valid[0], None
    scores = {id(c): 0.0 for c in valid}
    pair_scores = []
    for a, b in combinations(valid, 2):
        score = similarity(a.answer, b.answer)
        pair_scores.append(score)
        scores[id(a)] += score
        scores[id(b)] += score
    best = max(valid, key=lambda c: (scores[id(c)], -valid.index(c)))
    return best, sum(pair_scores) / len(pair_scores)


def provenance(package: dict, candidates: list[Candidate], chosen: Candidate | None, agreement: float | None,
               prompt_path: Path, model: str) -> dict:
    return {
        "arquivo": package["arquivo"],
        "sha256_gobr": package["sha256"],
        "versao_pacote": package["versao_pacote"],
        "prompt_sha256": hashlib.sha256(prompt_path.read_bytes()).hexdigest()[:12],
        "modelo": model,
        "gerador": "claude-code-subagent",
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "candidatos": {c.path.name: {"valido": c.report.ok, "erros": c.report.errors, "avisos": c.report.warnings}
                       for c in candidates},
        "escolhido": chosen.path.name if chosen else None,
        "concordancia": None if agreement is None else round(agreement, 3),
    }
