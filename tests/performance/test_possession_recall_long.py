"""B47 long-duration — possession recall remains stable."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_possession_recall_stable() -> None:
    eng = CognitiveEngine(agent_id="b47-long")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    pets = [("dog", "Zeus"), ("cat", "Luna"), ("dog", "Apollo")]
    for rel, name in pets:
        eng.encode(f"My {rel}'s name is {name}.", pin=True, provenance=TRUSTED_USER_STATEMENT)
        eng.sleep()
        out = eng.cognitive_respond(f"What's my {rel}'s name?")
        assert out["status"] == "known"
        assert name.lower() in (out.get("memory") or "").lower()
        assert "jeff" not in (out.get("memory") or "").lower()
    assert "jeff" in eng.cognitive_respond("Who am I?")["memory"].lower()
    assert "zeus" not in eng.cognitive_respond("Who am I?")["memory"].lower()
