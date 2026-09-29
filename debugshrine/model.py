from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable


STABLE = 0.35
LOCKED = 0.60


@dataclass
class AuditRecord:
    RecordId: str
    Timestamp: str
    Turn: str
    Intent: str
    ExpectedGate: str
    ActualGate: str
    GovernanceFlag: bool
    Notes: str = ""

    @property
    def RouteError(self) -> bool:
        return self.ExpectedGate != self.ActualGate

    @property
    def RouteDelta(self) -> str:
        return f"{self.ExpectedGate}→{self.ActualGate}"

    @property
    def Class(self) -> str:
        return classify(self)

    def to_public_dict(self) -> dict:
        d = asdict(self)
        d["RouteError"] = self.RouteError
        d["RouteDelta"] = self.RouteDelta
        d["Classification"] = self.Class
        return d


def classify(record: AuditRecord) -> str:
    if record.GovernanceFlag:
        return "GOVERNANCE"
    if record.RouteError:
        return "BOUNDARY"
    return "NORMAL"


def aggregate(records: Iterable[AuditRecord]) -> dict:
    recs = list(records)
    edges = Counter(r.RouteDelta for r in recs)
    nodes = Counter(r.ActualGate for r in recs)
    total = len(recs)
    if total == 0:
        return {
            "total": 0,
            "nodes": {},
            "edges": {},
            "dominant_edge": None,
            "dominant_ratio": 0.0,
            "surface": None,
        }
    dominant_edge, dominant_n = edges.most_common(1)[0]
    ratio = dominant_n / total
    return {
        "total": total,
        "nodes": dict(nodes),
        "edges": dict(edges),
        "dominant_edge": dominant_edge,
        "dominant_ratio": ratio,
        "surface": surface_band(ratio),
    }


def surface_band(ratio: float, stable: float = STABLE, locked: float = LOCKED) -> str:
    if ratio < stable:
        return "Stable"
    if ratio < locked:
        return "Emerging"
    return "Locked"
