"""C2 — High-impact assent apply (Gate B learning governance)."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.learning.model import AdaptationKind, AdaptationTarget, GovernanceClass
from acm.provenance import TRUSTED_USER_STATEMENT


def test_assent_applies_identity_confidence_delta() -> None:
    eng = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "assistant"},
    )
    eng.encode("My name is Jordan.", provenance=TRUSTED_USER_STATEMENT)
    user = eng.identity.schema_concept("user")
    assert user is not None
    before_conf = float(user.confidence)

    prop = eng.learning._propose(
        target_kind=AdaptationTarget.IDENTITY_CONCEPT,
        target_id=user.id,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        summary="High-impact identity contest requires assent.",
    )
    assert prop.governance == GovernanceClass.PROPOSED
    assert prop.applied is False
    assert prop.before.get("confidence") == before_conf
    assert prop.after.get("confidence", before_conf) < before_conf + 1e-9
    # Not applied until assent
    assert abs(float(user.confidence) - before_conf) < 1e-9

    exp_count = len(eng.store.experiences)
    result = eng.assent_adaptation(prop.id)
    assert result["status"] == "assented"
    assert abs(float(user.confidence) - float(prop.after["confidence"])) < 1e-6
    # Learning reorganizes living structure — never invents Experiences
    assert len(eng.store.experiences) == exp_count

    rolled = eng.rollback_adaptation(prop.id)
    assert rolled["status"] == "rolled_back"
    assert abs(float(user.confidence) - before_conf) < 1e-6


def test_reject_leaves_structure_unchanged() -> None:
    eng = CognitiveEngine(agent_id="reject")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    concept_id = next(iter(eng.store.concepts))
    concept = eng.store.concepts[concept_id]
    strength_before = concept.strength
    prop = eng.learning._propose(
        target_kind=AdaptationTarget.CONCEPT,
        target_id=concept_id,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        summary="Proposed weaken requires assent.",
    )
    rejected = eng.reject_adaptation(prop.id)
    assert rejected["status"] == "rejected"
    assert abs(concept.strength - strength_before) < 1e-9
    # Assent after reject must fail
    again = eng.assent_adaptation(prop.id)
    assert again["status"] == "not_proposed"


def test_assent_does_not_auto_apply_without_call() -> None:
    eng = CognitiveEngine(agent_id="no-auto")
    eng.encode("My name is Sam.", provenance=TRUSTED_USER_STATEMENT)
    user = eng.identity.schema_concept("user")
    conf = float(user.confidence)
    prop = eng.learning._propose(
        target_kind=AdaptationTarget.IDENTITY_CONCEPT,
        target_id=user.id,
        kind=AdaptationKind.WEAKEN,
        reflective_ids=[],
        summary="Needs assent.",
    )
    assert prop.governance == GovernanceClass.PROPOSED
    assert abs(float(user.confidence) - conf) < 1e-9
    pending = eng.what_have_i_learned()
    assert pending.get("pending_proposals") or any(
        a.get("governance") == "proposed"
        for a in (pending.get("adaptations") or pending.get("lessons") or [])
    ) or prop.id in eng.store.adaptations
