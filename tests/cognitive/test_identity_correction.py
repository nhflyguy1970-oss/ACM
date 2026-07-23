"""B20 — Identity correction & assent UX."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b20_preview_propose_assent_reject_cancel() -> None:
    eng = CognitiveEngine(agent_id="b20")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    preview = eng.preview_identity_change(key="name", value="Jeffrey", who="user")
    assert preview["status"] == "preview"
    assert preview["previous"] == "Jeff"
    assert preview["requires_assent"] is True
    assert preview["store_write"] is False

    prop = eng.propose_identity_change(key="name", value="Jeffrey", who="user")
    assert prop["status"] == "proposed"
    pid = prop["proposal"]["id"]
    pending = eng.pending_identity_changes()
    assert pending["count"] >= 1

    cancelled = eng.cancel_identity(pid)
    assert cancelled["cancelled"] is True
    # Name unchanged
    who = eng.cognitive_respond("Who am I?")
    assert "jeff" in (who.get("memory") or "").lower()

    prop2 = eng.propose_identity_change(key="name", value="Jeffrey", who="user")
    rejected = eng.reject_identity(prop2["proposal"]["id"])
    assert rejected["rejected"] is True

    prop3 = eng.propose_identity_change(key="name", value="Jeffrey", who="user")
    assented = eng.assent_identity(prop3["proposal"]["id"])
    assert assented["assented"] is True
    who2 = eng.cognitive_respond("Who am I?")
    assert "jeffrey" in (who2.get("memory") or "").lower()


def test_b20_apply_and_correction_and_isolation() -> None:
    eng = CognitiveEngine(
        agent_id="aria-b20",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.apply_identity_correction("My legal name changed to Jeffrey.")
    assert out["status"] == "applied"
    assert out["is_correction"] is True
    assert out["user_assistant_isolated"] is True
    # Assistant still Aria
    asst = eng.inspect_identity(who="assistant")
    assert "jeff" not in str(asst).lower() or asst.get("redaction_applied")
    spoken = eng.cognitive_respond("Who are you?")
    assert "aria" in (spoken.get("memory") or "").lower()
    # Collision blocked — user name must not land on assistant schema
    blocked = eng.preview_identity_change(key="name", value="Jeffrey", who="assistant")
    assert blocked["status"] == "blocked_collision"
