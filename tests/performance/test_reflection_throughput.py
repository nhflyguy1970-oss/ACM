from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_reflection_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-ref")
    for i in range(30):
        engine.encode(
            f"Fact {i} about module gamma relates to delta.",
            pin=True,
            provenance=TRUSTED_USER_STATEMENT,
        )
    t0 = perf_counter()
    for _ in range(15):
        engine.what_do_i_think("module gamma")
    elapsed = perf_counter() - t0
    assert engine.validation.snapshot()["reflection"]["reflections"] >= 15
    assert elapsed < 10.0
