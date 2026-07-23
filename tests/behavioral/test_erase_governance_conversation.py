"""B36 permanent behavioral conversation — forget assent UX."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_forget_address_requires_assent() -> None:
    eng = CognitiveEngine(agent_id="b36-beh")
    eng.encode("I live in Boston.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    preview = eng.preview_erase_request("Forget my old address.")
    assert preview["status"] == "preview"
    assert preview["requires_assent"] is True
    # Without assent, living memory remains
    prop = eng.propose_erase_request("Forget my old address.")
    assert prop["status"] == "proposed"
    user = eng.identity.schema_concept("user")
    assert any(a.active and a.key == "location" and "boston" in a.value.lower() for a in user.attributes)
    applied = eng.assent_erase_request(prop["proposal"]["id"])
    assert applied["status"] == "applied"
    assert applied["experiences_deleted"] is False
    user2 = eng.identity.schema_concept("user")
    assert not any(a.active and a.key == "location" for a in user2.attributes)
