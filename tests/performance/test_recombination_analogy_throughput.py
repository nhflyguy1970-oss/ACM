from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine


def test_recombination_analogy_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-ra")
    for i in range(8):
        engine.encode(f"Craft domain {i} uses specialized tools.", pin=True)
    t0 = perf_counter()
    for i in range(12):
        engine.what_new_memories_can_emerge(f"tools {i % 8}", blends=2)
        engine.what_is_analogous(f"domain {i % 8}", other=f"domain {(i + 1) % 8}")
    assert perf_counter() - t0 < 10.0
