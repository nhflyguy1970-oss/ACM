from __future__ import annotations

from acm import CognitiveEngine


def test_harness_reflection_metrics() -> None:
    engine = CognitiveEngine(agent_id="fobs")
    engine.encode("My favorite tea is green.", kind="preference")
    engine.what_do_i_think("What is my favorite tea?")
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    assert "reflection" in snap
    assert snap["reflection"]["reflections"] >= 1
    assert snap["reflection"]["reflective_experiences"] >= 1
    assert snap["reflection"]["activation_reused"] >= 1
    assert snap["counts"]["reflection_events"] >= 1


def test_insufficient_evidence_observable() -> None:
    engine = CognitiveEngine(agent_id="fobs")
    engine.what_do_i_think("obscure unused hapax topic")
    snap = engine.validation.snapshot()["reflection"]
    assert snap["reflections"] >= 1
    assert snap["insufficient_evidence"] >= 1 or snap["questions"] >= 1


def test_long_running_reflection_evolution() -> None:
    engine = CognitiveEngine(agent_id="fobs")
    for i in range(12):
        engine.encode(f"Practice session {i} improves woodworking skill.", pin=True)
    for _ in range(4):
        engine.what_do_i_think("woodworking")
    obs = engine.reflection.observables()
    assert obs["reflections"] >= 4
    assert engine.validation.snapshot()["reflection"]["reflective_experiences"] >= 4
    # Reflective Experiences accumulate without destroying prior practice Experiences
    kinds = [e.cognitive_kind.value for e in engine.store.experiences.values()]
    assert kinds.count("reflection") >= 4
    assert len(kinds) > kinds.count("reflection")
