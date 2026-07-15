from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine


def test_association_ingest_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-asc")
    t0 = perf_counter()
    for i in range(60):
        engine.encode(f"Alpha{i % 5} relates to Beta{i % 7}.", pin=True)
    elapsed = perf_counter() - t0
    assert engine.associations.observables()["association_count"] >= 5
    assert elapsed < 6.0
