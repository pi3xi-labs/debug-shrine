"""DebugShrine public method v1.0 — aggregate + classify."""

from collections import defaultdict


STABLE = 0.35
LOCKED = 0.60


def route_error(record):
    return record["ExpectedGate"] != record["ActualGate"]


def classify(record):
    if record["GovernanceFlag"]:
        return "GOVERNANCE"
    if route_error(record):
        return "BOUNDARY"
    return "NORMAL"


class TrajectoryAggregator:
    def __init__(self):
        self.node_count = defaultdict(int)
        self.edge_count = defaultdict(int)

    def add_record(self, expected, actual):
        self.node_count[actual] += 1
        self.edge_count[(expected, actual)] += 1

    def total(self):
        return sum(self.edge_count.values())

    def dominant_ratio(self):
        t = self.total()
        if t == 0:
            return 0.0
        return max(self.edge_count.values()) / t


def build_surface(agg):
    if agg.total() == 0:
        return None
    r = agg.dominant_ratio()
    if r < STABLE:
        return "Stable"
    if r < LOCKED:
        return "Emerging"
    return "Locked"
