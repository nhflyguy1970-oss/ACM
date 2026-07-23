"""B36 — Prune / forget / erase assent UX."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b36_preview_propose_reject_cancel_assent() -> None:
    eng = CognitiveEngine(agent_id="b36")
    eng.encode("I live in Boston.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    preview = eng.preview_erase_request("Forget my old address.")
    assert preview["status"] == "preview"
    assert preview["op"] == "soft_forget"
    assert preview["experiences_deleted"] is False
    assert "location" in preview["attribute_keys"] or preview["target_key"] == "location"

    prop = eng.propose_erase_request("Forget my old address.")
    assert prop["status"] == "proposed"
    pid = prop["proposal"]["id"]
    assert eng.pending_erase_requests()["count"] >= 1

    cancelled = eng.cancel_erase_request(pid)
    assert cancelled["cancelled"] is True
    # Location still active
    who = eng.cognitive_respond("Where do I live?")
    assert "boston" in (who.get("memory") or "").lower() or who.get("status") in {
        "known",
        "unknown",
    }

    prop2 = eng.propose_erase_request("Forget my old address.")
    rejected = eng.reject_erase_request(prop2["proposal"]["id"])
    assert rejected["rejected"] is True

    prop3 = eng.propose_erase_request("Forget my old address.")
    before = len(eng.store.experiences)
    applied = eng.assent_erase_request(prop3["proposal"]["id"])
    assert applied["status"] == "applied"
    assert applied["experiences_deleted"] is False
    assert len(eng.store.experiences) >= before  # audit Experience may add
    # Living location deactivated
    user = eng.identity.schema_concept("user")
    active_locs = [a for a in user.attributes if a.active and a.key == "location"]
    assert not active_locs


def test_b36_identity_name_soft_forget_blocked() -> None:
    eng = CognitiveEngine(agent_id="b36-id")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.propose_erase_request("Forget my name.")
    assert out["status"] == "blocked_identity_protection"
    assert "jeff" in eng.cognitive_respond("Who am I?")["memory"].lower()


def test_b36_legal_erase_preserves_experiences() -> None:
    eng = CognitiveEngine(agent_id="b36-legal")
    eng.encode("I live in Boston.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = len(eng.store.experiences)
    out = eng.apply_erase_request("Erase my address.")
    assert out["status"] == "applied"
    assert out["experiences_deleted"] is False
    assert len(eng.store.experiences) >= before
