from __future__ import annotations

from acm import CognitiveEngine


def test_long_running_learn_sleep_cycle_stable() -> None:
    engine = CognitiveEngine(agent_id="long")
    engine.encode("My favorite coffee is Ethiopian pour-over.", kind="preference", pin=True)
    engine.encode("Husky dogs love the snow.", pin=True)
    for i in range(15):
        engine.what_do_i_think("favorite coffee" if i % 2 == 0 else "husky")
        if i % 3 == 0:
            engine.learn(cue="favorite coffee" if i % 2 == 0 else "husky")
        if i % 4 == 0:
            engine.sleep()
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.9"
    # Experiences only grow via encode/reflect — not invented by sleep
    assert len(engine.store.experiences) >= 2
    for exp in engine.store.experiences.values():
        assert exp.summary  # content still present
    meta = engine.metacognitive_sketch()
    assert "learning" in meta
    assert "offline" in meta
