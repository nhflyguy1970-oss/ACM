"""B09 permanent behavioral conversation — diagnostic safety policy."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_diagnostics_never_leak_foreign_identity_or_store() -> None:
    """Conversation: inspect after teach must not leak assistant→user or store dumps."""
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is teal.", pin=True, provenance=TRUSTED_USER_STATEMENT)

    who = eng.inspect_identity(who="assistant")
    assert who["safety_policy_applied"] is True
    assert "jeff" not in str(who).lower()

    pref = eng.inspect_evidence("What is my favorite color?")
    assert pref["safety_policy_applied"] is True
    assert pref["redaction_applied"] is True
    assert "memory_store" not in str(pref).lower()
    assert "traceback" not in str(pref).lower()

    # Learning cert: policy never invents Experiences
    n = len(eng.store.experiences)
    eng.inspect("Who am I?")
    eng.organ_view("identity")
    assert len(eng.store.experiences) == n
