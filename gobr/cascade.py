"""First-match cascade over parametrization blocks (manual §7.6: a client parametrized by an earlier
block is not reprocessed by later ones).

Each block's own condition is a short union of boxes (a box is a conjunction of per-dimension
constraints; a composite source makes it a union, P8). The effective population of block k is its
own boxes minus the boxes of every earlier block that runs at least whenever k runs.
"""
from dataclasses import dataclass, field

from gobr import dims
from gobr.intervals import NEVER, IntervalSet
from gobr.ir import Block, GobrFile

Box = dict
# Narrow to wide: the last purchase with the seller is never more recent than the last purchase in the
# seller's group, which is never more recent than the last purchase with anyone in the company.
SCOPES_NARROW_TO_WIDE = ("vendedor", "grupo", "global")
MAX_RENDERED_BOXES = 3
SOURCE_PREFIXES = ("time", "carteira", "segmentacao:")


@dataclass
class Effective:
    block: Block
    own: list[Box]  # union of boxes; empty when the block's own filters contradict each other
    boxes: list[Box]
    treated_before: list[Block] = field(default_factory=list)  # earlier blocks that removed clients from this one
    partial_before: list[Block] = field(default_factory=list)  # earlier blocks that only run on some days

    @property
    def unreachable(self) -> bool:
        return not self.boxes


class Space:
    """Box algebra bound to one file (the 'time' dimension's domain is the file's team set)."""

    def value(self, box: Box, key: str):
        return box[key] if key in box else dims.domain(key)

    def intersect(self, a: Box, b: Box) -> Box | None:
        result = dict(a)
        for key, allowed in b.items():
            result[key] = self.value(a, key) & allowed
            if not result[key]:
                return None
        return result if self.feasible(result) else None

    def feasible(self, box: Box) -> bool:
        """Days since the last event must satisfy global <= grupo <= vendedor (never = infinitely long).
        Greedy: take the smallest admissible value scope by scope, from the widest scope inward."""
        for event in ("compra", "visita"):
            floor = 0.0
            for scope in reversed(SCOPES_NARROW_TO_WIDE):
                floor = _smallest_at_least(self.value(box, f"rec:{event}:{scope}"), floor)
                if floor is None:
                    return False
        return True

    def subtract(self, a: Box, b: Box) -> list[Box]:
        if self.intersect(a, b) is None:
            return [a]
        pieces, rest = [], dict(a)
        for key, allowed in b.items():
            current = self.value(rest, key)
            outside = current - allowed
            if outside and self.feasible({**rest, key: outside}):
                pieces.append({**rest, key: outside})
            rest[key] = current & allowed
        return pieces

    def simplify(self, boxes: list[Box]) -> list[Box]:
        """Drop unconstrained dimensions and merge boxes that differ in exactly one dimension."""
        boxes = [self._tighten({k: v for k, v in b.items() if v != dims.domain(k)}) for b in boxes]
        merged = True
        while merged:
            merged = False
            for i in range(len(boxes)):
                for j in range(i + 1, len(boxes)):
                    union = self._merge(boxes[i], boxes[j])
                    if union is not None:
                        boxes[i] = union
                        del boxes[j]
                        merged = True
                        break
                if merged:
                    break
        return boxes

    def _tighten(self, box: Box) -> Box:
        """Drop 'never' from a wider scope when a narrower scope already has a recorded event."""
        box = dict(box)
        for event in ("compra", "visita"):
            keys = [f"rec:{event}:{scope}" for scope in SCOPES_NARROW_TO_WIDE]
            for index, narrow in enumerate(keys):
                if narrow not in box or _longest(box[narrow]) == NEVER_DAYS:
                    continue
                for wide in keys[index + 1:]:
                    if wide in box:
                        box[wide] = box[wide] - IntervalSet.of(NEVER, NEVER)
        return box

    def _merge(self, a: Box, b: Box) -> Box | None:
        keys = set(a) | set(b)
        differing = [k for k in keys if self.value(a, k) != self.value(b, k)]
        if len(differing) != 1:
            return None
        key = differing[0]
        union = self.value(a, key) | self.value(b, key)
        merged = {**a, key: union}
        return {k: v for k, v in merged.items() if v != dims.domain(k)}


NEVER_DAYS = float("inf")  # 'never' sorts after any finite number of days (INF is only an open upper bound)


def _smallest_at_least(days: IntervalSet, floor: float) -> float | None:
    candidates = [max(lo, floor) for lo, hi in days.spans if lo != NEVER and hi >= floor]
    candidates += [max(0, floor) for lo, hi in days.spans if lo == NEVER and hi > NEVER and hi >= floor]
    if any(lo == NEVER for lo, _ in days.spans):
        candidates.append(NEVER_DAYS)
    return min(candidates) if candidates else None


def _longest(days: IntervalSet) -> float:
    if any(lo == NEVER for lo, _ in days.spans):
        return NEVER_DAYS
    return max(hi for _, hi in days.spans)


def own_boxes(block: Block, space: Space) -> list[Box]:
    boxes: list[Box] = [{}]
    for clause in block.sources + block.filters:
        options = clause.detail.get("alternativas", [clause.constraint])
        boxes = [box for b in boxes for o in options if (box := space.intersect(b, o)) is not None]
    return boxes


def temporal_key(block: Block) -> tuple[str, ...]:
    """Schedule identity of a block; empty means it runs on every execution."""
    return tuple(sorted(c.text for c in block.temporal if c.text != "todos os dias"))


def compute(file: GobrFile) -> list[Effective]:
    space = Space()
    consumers: list[tuple[Block, list[Box]]] = []
    results = []
    for block in file.of_kind("parametros", "limpar parametros"):
        own = own_boxes(block, space)
        effective = Effective(block, own, list(own))
        for earlier, boxes in consumers:
            if all(space.intersect(e, b) is None for e in effective.boxes for b in boxes):
                continue
            if temporal_key(earlier) and temporal_key(earlier) != temporal_key(block):
                effective.partial_before.append(earlier)
                continue
            effective.treated_before.append(earlier)
            effective.boxes = subtract_all(space, effective.boxes, boxes)
        results.append(effective)
        # P3: 'limpar parametros' resets parameters but parametrizes nobody, so it never consumes clients.
        if block.kind == "parametros" and own:
            consumers.append((block, own))
    return results


def subtract_all(space: Space, boxes: list[Box], removed: list[Box]) -> list[Box]:
    for box in removed:
        boxes = space.simplify([p for b in boxes for p in space.subtract(b, box)])
    return boxes


def source_box(box: Box) -> Box:
    return {k: v for k, v in box.items() if k.startswith(SOURCE_PREFIXES)}


def uncovered(effectives: list[Effective]) -> list[tuple[Effective, list[Box]]]:
    """Per distinct rule source (first rule that uses it): clients that no always-running block parametrizes."""
    space = Space()
    gaps, seen = [], []
    for first in effectives:
        universe = sources_of(first.own)
        if not universe or universe in seen:
            continue
        seen.append(universe)
        rest = universe
        for e in effectives:
            if e.own and not temporal_key(e.block) and e.block.kind == "parametros":
                rest = subtract_all(space, rest, e.own)
        if rest:
            gaps.append((first, rest))
    return gaps


def sources_of(boxes: list[Box]) -> list[Box]:
    unique: list[Box] = []
    for box in map(source_box, boxes):
        if box not in unique:
            unique.append(box)
    return unique


def render_boxes(boxes: list[Box], own: list[Box], numbers: set[int], hidden: set[str]) -> str | None:
    """pt-BR text for a union of boxes; None when it is too fragmented to be readable."""
    rendered = []
    for box in boxes:
        explicit_group = sum(k.startswith("rec:compra:") for k in box) > 1
        rendered.append([dims.render(k, v, numbers, explicit_group) for k, v in sorted(box.items(), key=_dimension_order)
                         if k not in hidden and not _is_own_source(k, v, own)])
    # Absorption (A or (A and B) = A): once source dimensions are hidden, a box whose visible parts
    # include all parts of another adds nothing to the text.
    kept = [parts for i, parts in enumerate(rendered)
            if not any(set(other) <= set(parts) and (set(other) < set(parts) or j < i)
                       for j, other in enumerate(rendered) if j != i)]
    if len(kept) > MAX_RENDERED_BOXES:
        return None
    texts = [" e ".join(parts) if parts else "todos os clientes" for parts in kept]
    return " OU ".join(f"({t})" for t in texts) if len(texts) > 1 else texts[0]


def _is_own_source(key: str, value, own: list[Box]) -> bool:
    return key.startswith(SOURCE_PREFIXES) and any(box.get(key) == value for box in own)


def _dimension_order(item) -> tuple[int, str]:
    key = item[0]
    rank = 0 if key.startswith("time") else 1 if key.startswith("rec:") else 2
    return rank, key
