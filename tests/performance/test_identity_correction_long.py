"""B20 long-duration — repeated identity corrections remain stable."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_identity_corrections_stable() -> None:
    eng = CognitiveEngine(agent_id="b20-long")
    eng.encode("My name is Alex.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    names = ["Alex", "Sam", "Jordan", "Casey", "Riley"]
    for i, name in enumerate(names[1:], start=1):
        out = eng.apply_identity_change(key="name", value=name, who="user", assent=True)
        assert out["status"] == "applied"
        if i % 2 == 0:
            eng.sleep()
    final = eng.inspect_identity(who="user")
    assert final.get("safety_policy_applied") is True or final.get("redaction")
    spoken = eng.cognitive_respond("Who am I?")
    assert "riley" in (spoken.get("memory") or "").lower()
    # Experience growth only from authorized encodes
    assert len(eng.store.experiences) >= len(names)
