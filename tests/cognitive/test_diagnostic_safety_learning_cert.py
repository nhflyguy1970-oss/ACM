"""B09 learning certification — diagnostic safety never invents memory (L25)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l25_diagnostic_safety_preserves_provenance_and_bounds() -> None:
    eng = CognitiveEngine(agent_id="m-l25")
    eng.encode("Bounded diagnostics matter.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    v1 = eng.inspect_evidence("Bounded diagnostics")
    v2 = eng.inspect_evidence("Bounded diagnostics")
    assert v1["safety_policy_applied"] is True
    assert v1.get("provenance") is not None
    assert len(v1.get("supporting_experiences") or []) <= 20
    assert v1["fingerprint"] == v2["fingerprint"]
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
