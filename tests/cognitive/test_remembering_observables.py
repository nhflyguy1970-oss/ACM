from __future__ import annotations

from acm import CognitiveEngine


def test_harness_remembering_metrics() -> None:
    engine = CognitiveEngine(agent_id="robs")
    engine.encode("My favorite tea is green.", kind="preference")
    engine.remember("What is my favorite tea?")
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    assert "remembering" in snap
    assert snap["remembering"]["reconstructions"] >= 1
    assert snap["remembering"]["activations"] >= 1
    assert snap["counts"]["remembering_events"] >= 1
    assert snap["remembering"]["evolution"]["touches"] >= 1


def test_activation_propagation_and_decay_observable() -> None:
    engine = CognitiveEngine(agent_id="robs")
    engine.encode("A robin is a bird.", pin=True)
    engine.encode("Birds migrate in seasons.", pin=True)
    result = engine.remember("robin")
    act = result.reconstruction["activation"]
    assert act["seed_count"] >= 1
    assert "decayed" in act
    snap = engine.validation.snapshot()["remembering"]
    assert snap["propagations"] >= 0
    assert snap["decays"] >= 0


def test_identity_influence_on_remembering() -> None:
    engine = CognitiveEngine(agent_id="robs")
    engine.encode("I am a research cartographer.", kind="identity", speaker="assistant")
    who = engine.remember("Who am I?")
    assert who.confidence >= 0
    assert "cartograph" in who.answer.lower() or who.activated_concept_ids
    snap = engine.validation.snapshot()
    assert snap["remembering"]["identity_influenced"] >= 1


def test_long_running_remember_evolution() -> None:
    engine = CognitiveEngine(agent_id="robs")
    for i in range(15):
        engine.encode(f"Practice session {i} improves fly tying skill.", pin=True)
    confidences = []
    for _ in range(5):
        confidences.append(engine.remember("fly tying").confidence)
    assert engine.remembering.observables()["reconstructions"] >= 5
    assert max(confidences) >= confidences[0]
    # Experiences remain count-stable under remember (no rewrite births)
    before = len(engine.store.experiences)
    engine.remember("fly tying")
    assert len(engine.store.experiences) == before
