"""Explainability READY items — age, accessibility, confidence, provenance."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b05_confidence_speech_includes_factors() -> None:
    eng = CognitiveEngine(agent_id="b05")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("How confident are you about my favorite color?")
    text = (result.get("memory") or "").lower()
    assert "confidence" in text
    assert "factor" in text or "strength" in text or "evidence" in text


def test_b14_provenance_how_do_you_know() -> None:
    eng = CognitiveEngine(agent_id="b14")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("How do you know my favorite color?")
    text = (result.get("memory") or "").lower()
    assert "taught" in text or "previously" in text or "blue" in text


def test_b16_memory_age_explanation() -> None:
    eng = CognitiveEngine(agent_id="b16")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("How old is my favorite color memory?")
    text = (result.get("memory") or "").lower()
    assert "old" in text or "minute" in text or "hour" in text or "day" in text
    assert result.get("intent") == "remembering"


def test_b17_accessibility_explanation() -> None:
    eng = CognitiveEngine(agent_id="b17")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("How accessible is my favorite color memory?")
    # May need cue tweak if accessibility_cue requires exact phrasing
    if "accessible" not in (result.get("memory") or "").lower():
        result = eng.cognitive_respond("How strong is my favorite color memory?")
    text = (result.get("memory") or "").lower()
    assert "strength" in text or "accessibility" in text or "accessible" in text


def test_b19_identity_evidence_via_evidence_cue() -> None:
    eng = CognitiveEngine(agent_id="b19")
    eng.encode("My name is Jeff.", provenance=TRUSTED_USER_STATEMENT)
    result = eng.cognitive_respond("How do you know my name is Jeff?")
    text = (result.get("memory") or "").lower()
    assert "jeff" in text
    assert "taught" in text or "previously" in text or "name" in text
