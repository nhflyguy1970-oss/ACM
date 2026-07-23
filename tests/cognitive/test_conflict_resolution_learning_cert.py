"""B13 learning certification — conflict confirm preserves provenance (L29)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l29_conflict_resolution_preserves_lineage() -> None:
    eng = CognitiveEngine(agent_id="m-l29")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is red.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prov_n = len(eng.store.provenance)
    opened = eng.open_conflict_resolution("favorite color", key="favorite_color")
    assert opened["status"] == "open"
    out = eng.confirm_conflict_resolution(opened["session"]["id"], "blue")
    assert out["lineage_preserved"] is True
    assert len(eng.store.provenance) >= prov_n
    assert eng.inspect_preference("color")["active"]["value"] == "blue"
