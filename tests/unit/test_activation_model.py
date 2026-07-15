from __future__ import annotations

from acm.activation import ActivationEngine, ActivationField, CueClass


def test_activation_field_public_has_no_reasoning() -> None:
    field = ActivationField(cue="coffee", cue_classes=[CueClass.QUESTION.value])
    pub = field.to_public()
    assert "reasoning" not in pub
    assert "prompt" not in pub
    assert pub["cue"] == "coffee"


def test_activation_engine_constants_are_explicit() -> None:
    assert ActivationEngine.DECAY < 1.0
    assert ActivationEngine.MAX_HOPS >= 1
    assert ActivationEngine.SEED_THRESHOLD > 0
