from __future__ import annotations

from acm.experiences.kinds import CognitiveKind, classify_cognitive_kind, normalize_external_kind
from acm.experiences.salience import SalienceVector


def test_cognitive_kind_classification() -> None:
    assert classify_cognitive_kind("Actually fix that") == CognitiveKind.CORRECTION
    assert classify_cognitive_kind("The test failed") == CognitiveKind.FAILURE
    assert classify_cognitive_kind("What is time?") == CognitiveKind.QUESTION
    assert (
        classify_cognitive_kind("hello", encode_kind="identity")
        == CognitiveKind.IDENTITY_CHANGE
    )


def test_external_kind_normalization() -> None:
    assert normalize_external_kind("IMAGE").value == "image"
    assert normalize_external_kind("nope").value == "other"


def test_salience_composite_bounds() -> None:
    v = SalienceVector(attention=2.0, novelty=-1.0).clamp()
    assert 0.0 <= v.attention <= 1.0
    assert 0.0 <= v.novelty <= 1.0
    assert 0.0 <= v.composite() <= 1.0
