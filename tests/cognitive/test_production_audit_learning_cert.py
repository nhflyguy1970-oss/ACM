"""L34 — Identity assent preserves Experience lineage (audit)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l34_identity_assent_preserves_experience_lineage() -> None:
    eng = CognitiveEngine(agent_id="m-l34")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before_exp = len(eng.store.experiences)
    before_prov = len(eng.store.provenance)
    prop = eng.propose_identity_change(key="name", value="Jeffrey", who="user")
    out = eng.assent_identity(prop["proposal"]["id"])
    assert out["assented"] is True
    assert out.get("experience_id")
    assert len(eng.store.experiences) > before_exp
    assert len(eng.store.provenance) >= before_prov
    # Reject invents nothing
    prop2 = eng.propose_identity_change(key="name", value="Bob", who="user")
    n = len(eng.store.experiences)
    eng.reject_identity(prop2["proposal"]["id"])
    assert len(eng.store.experiences) == n
