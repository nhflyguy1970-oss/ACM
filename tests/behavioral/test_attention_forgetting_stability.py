from __future__ import annotations

from acm import CognitiveEngine


def test_long_running_priority_accessibility_cycle() -> None:
    engine = CognitiveEngine(agent_id="long-af")
    coffee = engine.encode(
        "My favorite coffee is Ethiopian pour-over.", kind="preference", pin=True
    )["concept_id"]
    husky = engine.encode("Husky dogs love the snow.", pin=True)["concept_id"]
    exp_count = len(engine.store.experiences)
    for i in range(12):
        engine.remember("coffee" if i % 2 == 0 else "husky")
        if i % 3 == 0:
            engine.what_do_i_think("favorite coffee")
            engine.learn(cue="favorite coffee")
        if i % 4 == 0:
            engine.sleep()
        if i == 5:
            engine.cool_memory(husky, steps=3)
        if i == 8:
            engine.remember("husky")
    assert len(engine.store.experiences) >= exp_count  # never shrinks via cool
    assert engine.store.concepts[coffee].importance > 0.4
    # Husky should be recoverable
    assert engine.store.concepts[husky].active is True or "husky" in engine.remember(
        "husky"
    ).answer.lower()
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.10"
    assert "attention" in snap and "forgetting" in snap
    meta = engine.metacognitive_sketch()
    assert "attention" in meta and "forgetting" in meta
