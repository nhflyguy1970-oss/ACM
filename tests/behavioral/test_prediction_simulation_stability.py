from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_running_predict_simulate_cycle() -> None:
    engine = CognitiveEngine(agent_id="long-ps")
    engine.encode(
        "My favorite coffee is Ethiopian.",
        kind="preference",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    engine.encode("Breakfast precedes coffee.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp0 = len(engine.store.experiences)
    for i in range(10):
        engine.what_is_likely("coffee" if i % 2 == 0 else "breakfast")
        engine.what_futures_can_memory_imagine("morning routine", branches=2)
        if i % 3 == 0:
            engine.what_do_i_think("coffee")
            engine.learn(cue="coffee")
        if i % 4 == 0:
            engine.sleep()
        engine.encode(
            f"Morning note {i} about coffee cup.", pin=True, provenance=TRUSTED_USER_STATEMENT
        )
    assert len(engine.store.experiences) > exp0
    # Simulations never became experiences
    for sim in engine.store.simulations.values():
        assert sim.hypothetical is True
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    meta = engine.metacognitive_sketch()
    assert "prediction" in meta and "simulation" in meta
