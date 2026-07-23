"""B12 permanent behavioral conversation — preference correction."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_actually_red_explains_correction() -> None:
    eng = CognitiveEngine(agent_id="b12-beh")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.apply_preference_correction("Actually, my favorite color is red.")
    assert "corrected" in (out.get("explanation") or "").lower()
    assert "blue" in (out.get("explanation") or "").lower()
    spoken = eng.cognitive_respond("What is my favorite color?")
    assert "red" in (spoken.get("memory") or "").lower()
