from __future__ import annotations

from time import perf_counter

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_encode_remember_budget() -> None:
    engine = CognitiveEngine(agent_id="perf")
    t0 = perf_counter()
    for i in range(30):
        engine.encode(
            f"My favorite thing{i} is val{i}.", kind="preference", provenance=TRUSTED_USER_STATEMENT
        )
        engine.remember(f"What is my favorite thing{i}?")
    elapsed = perf_counter() - t0
    # Informative ceiling for M0 smoke on modest hardware
    assert elapsed < 5.0
