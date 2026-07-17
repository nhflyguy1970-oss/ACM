from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_prediction_simulation_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-ps")
    for i in range(8):
        engine.encode(
            f"Episode {i} toolkit pattern {i}.", pin=True, provenance=TRUSTED_USER_STATEMENT
        )
    t0 = perf_counter()
    for i in range(15):
        engine.what_is_likely(f"toolkit {i % 8}")
        engine.what_futures_can_memory_imagine(f"toolkit {i % 8}", branches=2)
    assert perf_counter() - t0 < 8.0
