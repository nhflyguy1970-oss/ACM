"""B12 — Preference correction UX."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_b12_actually_red_corrects_blue() -> None:
    eng = CognitiveEngine(agent_id="b12")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    preview = eng.preview_preference_correction("Actually, my favorite color is red.")
    assert preview["is_correction"] is True
    assert preview["previous"] == "blue"
    assert preview["proposed"] == "red"
    out = eng.apply_preference_correction("Actually, my favorite color is red.")
    assert out["status"] == "applied"
    assert out["is_correction"] is True
    assert eng.inspect_preference("color")["active"]["value"] == "red"
    eid = out["experience_id"]
    lineage = eng._preference_corrections.get(eid) or out.get("correction_lineage") or {}
    assert lineage.get("preference_correction") is True
    assert lineage.get("corrected_from") == "blue"


def test_b12_short_actually_uses_default_key() -> None:
    eng = CognitiveEngine(agent_id="b12-short")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    out = eng.apply_preference_correction("Actually, teal.")
    assert out["status"] == "applied"
    assert eng.inspect_preference("color")["active"]["value"] == "teal"
