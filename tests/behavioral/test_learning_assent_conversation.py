"""Permanent behavioral conversation — high-impact learning assent."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.learning.model import AdaptationKind, AdaptationTarget, GovernanceClass
from acm.provenance import TRUSTED_USER_STATEMENT


def test_behavioral_assent_then_rollback_preserves_provenance_and_history() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria"},
    )
    enc = eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    eid = enc["experience_id"]
    summary = eng.store.experiences[eid].summary
    meta = dict(eng.store.experiences[eid].metadata)

    user = eng.identity.schema_concept("user")
    conf0 = float(user.confidence)
    prop = eng.learning._propose(
        target_kind=AdaptationTarget.IDENTITY_CONCEPT,
        target_id=user.id,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        summary="Identity contest requires assent.",
    )
    assert prop.governance == GovernanceClass.PROPOSED

    # Host/user assents — living confidence changes; history intact
    assert eng.assent_adaptation(prop.id)["status"] == "assented"
    assert float(user.confidence) < conf0
    assert eng.store.experiences[eid].summary == summary
    assert dict(eng.store.experiences[eid].metadata) == meta

    # Reversible
    assert eng.rollback_adaptation(prop.id)["status"] == "rolled_back"
    assert abs(float(user.confidence) - conf0) < 1e-6
    assert eng.store.experiences[eid].summary == summary
