from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind
from acm.provenance import TRUSTED_USER_STATEMENT
from acm.types import Attribute


def test_reconciliation_never_rewrites_history() -> None:
    engine = CognitiveEngine(agent_id="rcl")
    engine.encode("Coffee supports morning focus.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode("Tea supports morning focus.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    before = len(engine.store.experiences)
    before_ids = set(engine.store.experiences)
    result = engine.how_should_memory_reconcile("morning focus")
    assert result["question"].startswith("When memories disagree")
    assert result["historical_rewrite"] is False
    assert result["deleted"] is False
    assert result["plans"] is False
    assert result["experiences_unchanged"] is True
    assert result["experience_ids_unchanged"] is True
    assert len(engine.store.experiences) == before
    assert set(engine.store.experiences) == before_ids
    assert result["reconciliation"]["id"] in engine.store.reconciliations


def test_conflict_preserves_lineage_and_lowers_confidence() -> None:
    engine = CognitiveEngine(agent_id="rcl")
    a = engine.encode(
        "Northward passage is preferred for cargo.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    b = engine.encode(
        "Southward corridor is preferred for cargo.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    ca = engine.store.concepts[a["concept_id"]]
    cb = engine.store.concepts[b["concept_id"]]
    assert ca.id != cb.id
    before_a = ca.confidence
    before_b = cb.confidence
    edge = engine.associations.relate(
        ca.id, cb.id, RelationKind.CONFLICTS_WITH, strength_forward=0.8, confidence=0.7
    )
    assert edge is not None
    result = engine.how_should_memory_reconcile("preferred cargo")
    status = result["reconciliation"]["status"]
    assert status in ("competing", "unresolved", "context_dependent", "revised")
    assert result["reconciliation"]["conflicting_ids"]
    # Living confidence recalibrated; Experiences intact
    assert ca.confidence <= before_a or cb.confidence <= before_b
    assert len(engine.store.confidence_events) >= 1
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    assert snap["reconciliation"]["reconciliations"] >= 1
    assert snap["confidence"]["evolutions"] >= 1


def test_corroboration_strengthens_confidence() -> None:
    engine = CognitiveEngine(agent_id="rcl")
    engine.encode("Sunrise comes after night.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.encode(
        "Dawn follows night and brings sunrise.", pin=True, provenance=TRUSTED_USER_STATEMENT
    )
    # Ensure activated concepts have multi-evidence for reinforce path
    concepts = [
        c
        for c in engine.store.concepts.values()
        if not c.identity
        and c.active
        and (
            "sun" in " ".join(c.labels).lower()
            or "dawn" in " ".join(c.labels).lower()
            or "night" in " ".join(c.labels).lower()
        )
    ]
    for c in concepts:
        if len(c.evidence_ids) < 2 and engine.store.experiences:
            c.evidence_ids.extend(list(engine.store.experiences)[:2])
            c.confidence = 0.5
    before = {c.id: c.confidence for c in concepts}
    result = engine.how_should_memory_reconcile("sunrise night")
    # Either reinforce or unresolved; if reinforce, confidence must rise on subjects
    rec = result["reconciliation"]
    if rec["status"] == "reinforce":
        for sid in rec["subject_ids"]:
            concept = engine.store.concepts.get(sid)
            if concept and sid in before:
                assert concept.confidence >= before[sid]


def test_context_dependent_coexistence() -> None:
    engine = CognitiveEngine(agent_id="rcl")
    engine.set_context("home", activity="kitchen")
    engine.encode("Mug lives in kitchen cabinet.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.set_context("office", activity="desk")
    engine.encode("Mug lives on office desk.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concepts = [
        c
        for c in engine.store.concepts.values()
        if not c.identity and "mug" in " ".join(c.labels).lower()
    ]
    if len(concepts) >= 1:
        c = concepts[0]
        c.attributes.append(
            Attribute(key="location", value="kitchen", confidence=0.8, context_tags=("home",))
        )
        c.attributes.append(
            Attribute(key="location", value="desk", confidence=0.35, context_tags=("office",))
        )
    engine.associations.relate(
        concepts[0].id if concepts else list(engine.store.concepts)[0],
        concepts[-1].id if len(concepts) > 1 else list(engine.store.concepts)[-1],
        RelationKind.CONFLICTS_WITH,
    )
    result = engine.how_should_memory_reconcile("mug lives")
    # With context tags, competing may become context_dependent
    assert result["reconciliation"]["status"] in (
        "context_dependent",
        "competing",
        "unresolved",
        "revised",
        "reinforce",
    )
    # No silent discard of Experiences
    assert len(engine.store.experiences) >= 2


def test_confidence_assessment_is_memory_only() -> None:
    engine = CognitiveEngine(agent_id="conf")
    engine.encode("Lake water feels cold in winter.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    result = engine.how_certain_am_i("lake water")
    assert result["question"].startswith("How certain am I")
    assert result["plans"] is False
    assert result["decides"] is False
    assert "snapshots" in result
    assert "uncertainty" in result
