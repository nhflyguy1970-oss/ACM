from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_attention_forgetting_throughput() -> None:
    engine = CognitiveEngine(agent_id="perf-af")
    ids = []
    for i in range(12):
        ids.append(
            engine.encode(
                f"Episode {i} about toolkit {i}.", pin=True, provenance=TRUSTED_USER_STATEMENT
            )["concept_id"]
        )
    t0 = perf_counter()
    for cid in ids:
        engine.attention.what_deserves_attention()
        engine.cool_memory(cid, steps=1)
        engine.reactivate_memory(cid, steps=1)
        engine.remember("toolkit")
    elapsed = perf_counter() - t0
    assert elapsed < 6.0
