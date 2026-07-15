from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine


def test_learning_throughput_smoke() -> None:
    engine = CognitiveEngine(agent_id="perf-learn")
    engine.encode("Favorite coffee is Ethiopian.", kind="preference", pin=True)
    thought = engine.what_do_i_think("favorite coffee")
    t0 = perf_counter()
    for _ in range(20):
        engine.learn(reflective_experience_id=thought["reflective_experience_id"])
    elapsed = perf_counter() - t0
    assert elapsed < 5.0


def test_offline_throughput_smoke() -> None:
    engine = CognitiveEngine(agent_id="perf-sleep")
    for i in range(8):
        engine.encode(f"Episode about module {i} firmware.", pin=True)
        engine.what_do_i_think(f"module {i}")
    t0 = perf_counter()
    for _ in range(10):
        engine.sleep()
    elapsed = perf_counter() - t0
    assert elapsed < 8.0
