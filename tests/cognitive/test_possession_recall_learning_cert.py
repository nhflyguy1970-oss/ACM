"""B47 learning certification — possession recall read-only (L33)."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l33_possession_recall_read_only_no_identity_write() -> None:
    eng = CognitiveEngine(agent_id="m-l33")
    eng.encode("My name is Jeff.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My dog's name is Zeus.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = len(eng.store.experiences)
    out = eng.present_possession_recall("What's my dog's name?")
    assert out["status"] == "known"
    assert out["invents_experiences"] is False
    assert out["store_write"] is False
    assert len(eng.store.experiences) == before
    user = eng.identity.schema_concept("user")
    names = [a.value for a in user.attributes if a.active and a.key == "name"]
    assert names == ["Jeff"]
