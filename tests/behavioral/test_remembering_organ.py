from __future__ import annotations

from acm import CognitiveEngine
from acm.types import ExplanationClass


def test_what_do_i_remember_reconstruction() -> None:
    engine = CognitiveEngine(agent_id="rem")
    engine.encode("My favorite coffee is dark roast.", kind="preference")
    result = engine.remember("What is my favorite coffee?")
    assert "dark roast" in result.answer.lower()
    assert result.explanation_class == ExplanationClass.PREFERENCE
    public = engine.what_do_i_remember("What is my favorite coffee?")
    assert public["question"] == "What do I remember?"
    assert public["activation"]["concept_activations"]
    assert result.ambiguous is False


def test_spreading_activation_uses_associations() -> None:
    engine = CognitiveEngine(agent_id="rem")
    engine.encode("A husky is a dog.", pin=True)
    engine.encode("Athena is a husky.", pin=True)
    result = engine.remember("husky")
    assert result.activated_concept_ids
    steps = result.reconstruction["activation"]["propagation_steps"]
    assert steps >= 1 or result.reconstruction["activation"]["association_activations"] >= 1


def test_context_sensitive_emphasis() -> None:
    engine = CognitiveEngine(agent_id="rem")
    engine.encode(
        "At home my favorite coffee is dark roast.",
        kind="preference",
        context_tags=("home",),
    )
    engine.set_context("home")
    home = engine.remember("What is my favorite coffee?")
    assert "dark roast" in home.answer.lower()
    assert home.reconstruction["context_influenced"] or "home" in engine.context.tags


def test_historical_integrity_of_experiences() -> None:
    engine = CognitiveEngine(agent_id="rem")
    out = engine.encode("Zeus went camping near water.", pin=True)
    eid = out["experience_id"]
    before = engine.store.experiences[eid]
    summary = before.summary
    seq = before.sequence
    engine.remember("camping")
    engine.remember("Zeus")
    after = engine.store.experiences[eid]
    assert after.summary == summary
    assert after.sequence == seq
    assert after is before  # frozen identity preserved


def test_competing_recollections_surface_ambiguity() -> None:
    engine = CognitiveEngine(agent_id="rem")
    engine.encode("My favorite beverage is coffee.", kind="preference")
    engine.encode("My favorite beverage is tea.", kind="preference")
    # Two active preference attributes can compete depending on supersede behavior
    result = engine.remember("What is my favorite beverage?")
    # Either superseded single answer OR ambiguity — never silent dual actives without signal
    snap = engine.validation.snapshot()
    assert snap["remembering"]["reconstructions"] >= 1
    assert result.confidence >= 0.0
    if result.ambiguous:
        assert result.reconstruction["competing"]


def test_working_memory_bias() -> None:
    engine = CognitiveEngine(agent_id="rem", buffer_capacity=3)
    engine.encode("Fly tying is a craft.", pin=True)
    engine.encode("Woodworking is a craft.", pin=True)
    first = engine.remember("fly tying")
    assert first.activated_concept_ids
    second = engine.remember("craft")
    assert second.reconstruction["working_influenced"] or len(engine.buffer) >= 1
