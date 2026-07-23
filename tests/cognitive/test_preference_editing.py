"""B11 — Preference editing UX."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b11_inspect_preview_set_replace_remove() -> None:
    eng = CognitiveEngine(agent_id="b11")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    listed = eng.inspect_preferences()
    assert listed["count"] >= 1
    assert any(p["key"] == "favorite_color" for p in listed["preferences"])
    one = eng.inspect_preference("color")
    assert one["known"] is True
    assert one["active"]["value"] == "blue"

    preview = eng.preview_preference_change(key="color", value="red", op="set")
    assert preview["store_write"] is False
    assert preview["previous"] == "blue"
    assert preview["proposed"] == "red"
    assert preview["op"] == "replace"

    applied = eng.apply_preference_change(key="color", value="red", op="set")
    assert applied["status"] == "applied"
    assert eng.inspect_preference("color")["active"]["value"] == "red"

    # Unrelated preference isolation
    eng.encode("My favorite tea is oolong.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.apply_preference_change(key="color", value="green")
    assert eng.inspect_preference("tea")["active"]["value"] == "oolong"

    removed = eng.apply_preference_change(key="color", op="remove")
    assert removed["status"] == "applied"
    assert eng.inspect_preference("color")["known"] is False


def test_b11_propose_assent_reject_cancel() -> None:
    eng = CognitiveEngine(agent_id="b11-gate")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prop = eng.propose_preference_change(key="color", value="teal")
    assert prop["status"] == "proposed"
    pid = prop["proposal"]["id"]
    # Cancel path
    cancelled = eng.cancel_preference_change(pid)
    assert cancelled["status"] == "cancelled"
    assert eng.inspect_preference("color")["active"]["value"] == "blue"

    prop2 = eng.propose_preference_change(key="color", value="red")
    rejected = eng.reject_preference_change(prop2["proposal"]["id"])
    assert rejected["status"] == "rejected"
    assert eng.inspect_preference("color")["active"]["value"] == "blue"

    prop3 = eng.propose_preference_change(key="color", value="purple")
    assented = eng.assent_preference_change(prop3["proposal"]["id"])
    assert assented["status"] == "applied"
    assert eng.inspect_preference("color")["active"]["value"] == "purple"
