"""M5 Cap1 performance benchmarks — hierarchy ops stay bounded."""

from __future__ import annotations

import time

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_hierarchy_query_benchmark_under_budget() -> None:
    eng = CognitiveEngine(agent_id="m5-perf")
    for i in range(20):
        eng.encode(f"Item{i} is a gadget.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    t0 = time.perf_counter()
    for _ in range(50):
        eng.concept_hierarchy("gadget")
        eng.concept_hierarchy("item0")
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    # Deterministic in-memory queries — generous budget for CI variance.
    assert elapsed_ms < 2000.0, f"hierarchy queries too slow: {elapsed_ms:.1f}ms"
