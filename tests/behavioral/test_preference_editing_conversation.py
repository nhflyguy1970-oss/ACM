"""B11 permanent behavioral conversation — preference editing UX."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_change_favorite_color_with_preview_and_lineage() -> None:
    eng = CognitiveEngine(agent_id="b11-beh")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    preview = eng.preview_preference_change(key="favorite_color", value="red")
    assert "blue" in preview["previous"]
    assert "red" in preview["proposed"]
    out = eng.apply_preference_change(key="favorite_color", value="red")
    assert out["status"] == "applied"
    assert out["lineage_preserved"] is True
    versions = eng.inspect_preference("favorite_color")["versions"]
    assert any(v["value"] == "blue" and not v["active"] for v in versions)
    assert any(v["value"] == "red" and v["active"] for v in versions)
    spoken = eng.cognitive_respond("What is my favorite color?")
    assert "red" in (spoken.get("memory") or "").lower()
