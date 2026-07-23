"""B13 permanent behavioral conversation — assisted conflict resolution."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_which_is_current_blue_or_red() -> None:
    eng = CognitiveEngine(agent_id="b13-beh")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is red.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    opened = eng.open_conflict_resolution("What is my favorite color?")
    assert opened["status"] == "open"
    out = eng.confirm_conflict_resolution(opened["session"]["id"], "red")
    assert out["status"] == "confirmed"
    spoken = eng.cognitive_respond("What is my favorite color?")
    assert "red" in (spoken.get("memory") or "").lower()
