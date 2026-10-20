"""Closed integer interval sets, used for day-based dimensions (recency, historical frequency).

The value -1 encodes "no record" (never bought / never visited / undefined frequency), so a
dimension's full domain is [-1, INF].
"""
from dataclasses import dataclass

INF = 10**9
NEVER = -1


@dataclass(frozen=True)
class IntervalSet:
    spans: tuple[tuple[int, int], ...] = ()

    @staticmethod
    def of(lo: int, hi: int = INF) -> "IntervalSet":
        return IntervalSet(((lo, hi),)) if lo <= hi else IntervalSet()

    @staticmethod
    def full() -> "IntervalSet":
        return IntervalSet.of(NEVER, INF)

    @staticmethod
    def _normalized(spans) -> "IntervalSet":
        merged: list[list[int]] = []
        for lo, hi in sorted(s for s in spans if s[0] <= s[1]):
            if merged and lo <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], hi)
            else:
                merged.append([lo, hi])
        return IntervalSet(tuple((lo, hi) for lo, hi in merged))

    def __or__(self, other: "IntervalSet") -> "IntervalSet":
        return IntervalSet._normalized(self.spans + other.spans)

    def __and__(self, other: "IntervalSet") -> "IntervalSet":
        return IntervalSet._normalized(
            (max(a, c), min(b, d)) for a, b in self.spans for c, d in other.spans
        )

    def __sub__(self, other: "IntervalSet") -> "IntervalSet":
        return self & other.complement()

    def complement(self) -> "IntervalSet":
        gaps, cursor = [], NEVER
        for lo, hi in self.spans:
            if lo > cursor:
                gaps.append((cursor, lo - 1))
            cursor = max(cursor, hi + 1)
        if cursor <= INF:
            gaps.append((cursor, INF))
        return IntervalSet._normalized(gaps)

    def __bool__(self) -> bool:
        return bool(self.spans)
