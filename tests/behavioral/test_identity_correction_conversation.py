"""B20 permanent behavioral conversation — identity correction assent."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_legal_name_change_requires_explicit_path() -> None:
    eng = CognitiveEngine(agent_id="b20-beh")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    preview = eng.preview_identity_correction("My legal name changed to Jeffrey Richardson.")
    assert preview["status"] == "preview"
    assert "jeffrey" in preview["proposed"].lower()
    out = eng.apply_identity_correction("My legal name changed to Jeffrey Richardson.")
    assert out["status"] == "applied"
    spoken = eng.cognitive_respond("Who am I?")
    mem = (spoken.get("memory") or "").lower()
    assert "jeffrey" in mem
