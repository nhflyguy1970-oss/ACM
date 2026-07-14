from __future__ import annotations

from acm import CognitiveEngine


def test_supersede_preference(engine: CognitiveEngine) -> None:
    engine.encode("My favorite coffee is dark roast.", kind="preference")
    engine.encode("My favorite coffee is medium roast.", kind="preference")
    result = engine.remember("What is my favorite coffee?")
    assert "medium roast" in result.answer.lower()
    assert "dark roast" not in result.answer.lower()
    assert any(r.get("kind") == "supersede" for r in engine.validation.reconsolidations)


def test_remember_strengthens(engine: CognitiveEngine) -> None:
    engine.encode("My favorite tea is green.", kind="preference")
    first = engine.remember("What is my favorite tea?")
    second = engine.remember("What is my favorite tea?")
    assert second.confidence >= first.confidence
    assert engine.validation.reconsolidations
