from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_experience_birth_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-exp")
    t0 = perf_counter()
    for i in range(100):
        engine.encode(
            f"Timed observation {i} in the stream.", pin=True, provenance=TRUSTED_USER_STATEMENT
        )
    elapsed = perf_counter() - t0
    assert len(engine.what_happened(limit=100)) == 100
    assert elapsed < 5.0
