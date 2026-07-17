from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_concept_ingest_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-con")
    t0 = perf_counter()
    for i in range(80):
        engine.encode(f"Item{i} is a gadget.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    elapsed = perf_counter() - t0
    assert engine.concepts.observables()["concept_count"] >= 10
    assert elapsed < 5.0
