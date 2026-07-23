"""B20 learning certification — identity correction preserves provenance (L30)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l30_identity_correction_preserves_provenance_and_isolation() -> None:
    eng = CognitiveEngine(
        agent_id="m-l30",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prov_n = len(eng.store.provenance)
    exp_n = len(eng.store.experiences)
    out = eng.apply_identity_correction("Call me Jeffrey.")
    assert out["status"] == "applied"
    assert len(eng.store.provenance) >= prov_n
    assert len(eng.store.experiences) > exp_n
    # Reject path does not invent Experiences
    prop = eng.propose_identity_change(key="name", value="Bob", who="user")
    before = len(eng.store.experiences)
    eng.reject_identity(prop["proposal"]["id"])
    assert len(eng.store.experiences) == before
    asst = eng.cognitive_respond("Who are you?")
    assert "bob" not in (asst.get("memory") or "").lower()
    assert "jeff" not in (asst.get("memory") or "").lower()
