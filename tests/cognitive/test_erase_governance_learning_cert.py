"""B36 learning certification — erase never deletes Experiences (L32)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l32_erase_preserves_experiences_and_provenance() -> None:
    eng = CognitiveEngine(agent_id="m-l32")
    eng.encode("I live in Boston.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite color is blue.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before_exp = len(eng.store.experiences)
    before_prov = len(eng.store.provenance)
    out = eng.apply_erase_request("Forget my favorite color.")
    assert out["status"] == "applied"
    assert out["experiences_deleted"] is False
    assert len(eng.store.experiences) >= before_exp
    assert len(eng.store.provenance) >= before_prov
    # Reject invents nothing
    prop = eng.propose_erase_request("Forget my old address.")
    n = len(eng.store.experiences)
    eng.reject_erase_request(prop["proposal"]["id"])
    assert len(eng.store.experiences) == n
