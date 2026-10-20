"""Intermediate representation of a parsed .gobr file."""
from dataclasses import dataclass, field


@dataclass
class Clause:
    text: str  # normalized source text (accents folded, literals restored)
    gloss: str  # pt-BR meaning; empty when the clause was not recognized
    recognized: bool = True
    constraint: dict = field(default_factory=dict)  # dimension key -> allowed values (see dims.py)
    numbers: list[int] = field(default_factory=list)  # thresholds a description must mention
    detail: dict = field(default_factory=dict)  # structured extras (e.g. weekday preferences)


@dataclass
class Block:
    id: str
    kind: str  # time | carteira | carteira livre | segmentacao | parametros | limpar parametros | alerta | tag
    name: str
    line_no: int
    sources: list[Clause] = field(default_factory=list)
    temporal: list[Clause] = field(default_factory=list)
    filters: list[Clause] = field(default_factory=list)
    actions: list[Clause] = field(default_factory=list)
    unclassified: list[str] = field(default_factory=list)

    @property
    def schedules_nothing(self) -> bool:
        return any(a.detail.get("tipo") == "nao_agendar" for a in self.actions)

    def all_clauses(self) -> list[Clause]:
        return self.sources + self.temporal + self.filters + self.actions


@dataclass
class GobrFile:
    header_comments: list[str]
    blocks: list[Block]
    teams: dict[str, frozenset[str]]  # source name (time/carteira/segmentacao) -> root team names

    def of_kind(self, *kinds: str) -> list[Block]:
        return [b for b in self.blocks if b.kind in kinds]
