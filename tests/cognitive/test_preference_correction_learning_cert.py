"""B12 learning certification — correction lineage (L28)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l28_preference_correction_lineage() -> None:
    eng = CognitiveEngine(agent_id="m-l28")
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prov_n = len(eng.store.provenance)
    out = eng.apply_preference_correction("Actually, my favorite color is red.")
    assert out["is_correction"] is True
    assert len(eng.store.provenance) >= prov_n
    versions = eng.inspect_preference("color")["versions"]
    assert any(v["value"] == "blue" and not v["active"] for v in versions)
    assert any(v["value"] == "red" and v["active"] for v in versions)
