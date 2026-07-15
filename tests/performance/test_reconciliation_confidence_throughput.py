from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine


def test_reconciliation_confidence_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-rcl")
    for i in range(8):
        engine.encode(f"Beacon channel {i} reports weather.", pin=True)
    t0 = perf_counter()
    for i in range(12):
        engine.how_should_memory_reconcile(f"beacon {i % 8}")
        engine.how_certain_am_i(f"weather {i % 8}")
    assert perf_counter() - t0 < 10.0
