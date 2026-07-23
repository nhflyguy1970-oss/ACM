"""B13 — User-assisted conflict resolution."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b13_confirm_rejects_and_abstain() -> None:
    eng = CognitiveEngine(agent_id="b13")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is red.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    opened = eng.open_conflict_resolution("What is my favorite color?", key="color")
    assert opened["status"] == "open"
    sess = opened["session"]
    assert len(sess["options"]) >= 2
    assert "Which is current?" in sess["prompt"]

    # Abstain leaves living preference as last encode (red)
    abstained = eng.abstain_conflict_resolution(sess["id"])
    assert abstained["status"] == "abstained"
    assert eng.inspect_preference("color")["active"]["value"] == "red"

    opened2 = eng.open_conflict_resolution("What is my favorite color?", key="color")
    rejected = eng.reject_conflict_resolution(opened2["session"]["id"])
    assert rejected["status"] == "rejected"

    opened3 = eng.open_conflict_resolution("What is my favorite color?", key="color")
    confirmed = eng.confirm_conflict_resolution(opened3["session"]["id"], "blue")
    assert confirmed["status"] == "confirmed"
    assert confirmed["historical_rewrite"] is False
    assert eng.inspect_preference("color")["active"]["value"] == "blue"
    # Prior red retained in versions
    versions = eng.inspect_preference("color")["versions"]
    assert any(v["value"] == "red" for v in versions)
