"""Behavioral audit — read-only and assent provenance must hold under stress."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.authority.mode import read_only
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_audit_governance_write_spine() -> None:
    eng = CognitiveEngine(
        agent_id="aria-audit",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    # Inspect-style read_only must not allow silent encode
    with read_only():
        blocked = eng.encode("My name is Eve.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    assert blocked.get("reason") == "read_only_blocked"
    assert "jeff" in eng.cognitive_respond("Who am I?")["memory"].lower()

    prop = eng.propose_identity_change(key="name", value="Jeffrey", who="user")
    assented = eng.assent_identity(prop["proposal"]["id"])
    assert assented["assented"] is True
    assert assented.get("experience_id")
    assert "jeffrey" in eng.cognitive_respond("Who am I?")["memory"].lower()
    assert "aria" in eng.cognitive_respond("Who are you?")["memory"].lower()
