from __future__ import annotations

from acm import CognitiveEngine


def test_m0_harness_records_activation_and_lifecycle(engine: CognitiveEngine) -> None:
    engine.encode("My favorite coffee is dark roast.", kind="preference")
    engine.remember("What is my favorite coffee?")
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.3"
    assert snap["counts"]["activations"] >= 1
    assert snap["counts"]["lifecycle"] >= 1
    assert snap["counts"]["reconsolidations"] >= 1
    assert snap["activations"][-1]["cue"]


def test_identity_touch(engine: CognitiveEngine) -> None:
    engine.encode("I am a coding assistant that helps with memory research.", kind="identity")
    assert engine.validation.identity_touches
    sketch = engine.metacognitive_sketch()
    assert sketch["what_i_know_count"] >= 1
    assert "identity_concepts" in sketch


def test_working_transitions_under_pressure() -> None:
    engine = CognitiveEngine(agent_id="wm", buffer_capacity=3)
    for i in range(6):
        engine.encode(f"My favorite snack{i} is item{i}.", kind="preference")
    assert any(t.action == "displace" for t in engine.validation.working_transitions)


def test_no_chain_of_thought_in_public_trace(engine: CognitiveEngine) -> None:
    engine.encode("My favorite color is blue.", kind="preference")
    result = engine.remember("favorite color?")
    blob = str(result.trace).lower()
    assert "chain of thought" not in blob
    assert "prompt" not in blob
    assert result.trace.get("explanation_class")
