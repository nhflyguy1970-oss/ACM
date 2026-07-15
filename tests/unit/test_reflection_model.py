from __future__ import annotations

from acm.reflection.model import ReflectionEvaluation, ReflectionOutcome


def test_reflection_public_has_no_reasoning() -> None:
    ev = ReflectionEvaluation(
        cue="coffee",
        remembered_answer="dark roast",
        remembered_confidence=0.7,
        confidence_assessment=0.65,
        outcomes=[ReflectionOutcome.SUFFICIENT, ReflectionOutcome.INSIGHT],
        evaluation_summary="Consistent recollection.",
    )
    pub = ev.to_public()
    assert pub["question"] == "What do I think about what I remember?"
    assert "reasoning" not in pub
    assert "prompt" not in pub
    assert "chain" not in str(pub).lower()
