from __future__ import annotations

from acm import CognitiveEngine
from acm.types import ExplanationClass


def test_encode_preference_and_remember(engine: CognitiveEngine) -> None:
    out = engine.encode("My favorite coffee is dark roast.", kind="preference")
    assert out["encoded"] is True
    result = engine.remember("What is my favorite coffee?")
    assert "dark roast" in result.answer.lower()
    assert result.explanation_class == ExplanationClass.PREFERENCE
    assert "preference" in result.explanation.lower()
    assert result.confidence > 0.5


def test_low_attention_skips_ordinary_chatter(engine: CognitiveEngine) -> None:
    out = engine.encode("um okay sure")
    assert out["encoded"] is False
    assert out["reason"] == "low_attention"


def test_unknown_when_empty(engine: CognitiveEngine) -> None:
    result = engine.remember("What is my favorite tea?")
    assert result.explanation_class == ExplanationClass.UNKNOWN
    assert result.confidence == 0.0
