from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine


def test_remember_activation_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-rem")
    for i in range(40):
        engine.encode(f"Fact {i} about module alpha relates to beta.", pin=True)
    t0 = perf_counter()
    for _ in range(20):
        engine.remember("module alpha")
    elapsed = perf_counter() - t0
    assert engine.validation.snapshot()["remembering"]["reconstructions"] >= 20
    assert elapsed < 8.0
