"""M5 Cap2 — Evidence weighting & decay (never delete provenance)."""

from __future__ import annotations

from time import time

from acm import CognitiveEngine
from acm.confidence.model import EvidenceStatus, UncertaintyKind
from acm.provenance import TRUSTED_USER_STATEMENT


def test_evidence_accumulates_and_ages_without_deleting_provenance() -> None:
    eng = CognitiveEngine(agent_id="m5-ev")
    eng.encode("My favorite tea is oolong.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite tea is oolong.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    prefs = [
        c
        for c in eng.store.concepts.values()
        if any(a.key.startswith("favorite_tea") and a.active for a in c.attributes)
    ]
    assert prefs
    concept = prefs[0]
    prov_before = len(eng.store.provenance)
    exp_before = len(eng.store.experiences)
    evid_before = list(concept.evidence_ids)

    # Seed influences as aged (encode may have just reinforced them).
    past = time() - 40 * 86400
    for eid in concept.evidence_ids:
        inf = eng.confidence._ensure_influence("concept", concept.id, eid, now=past)
        inf.last_reinforced = past
        inf.created = past
        inf.weight = 1.0
        eng.store.evidence_influences[inf.key] = inf
    snap1 = eng.confidence.estimate_concept(concept.id)
    mass1 = snap1.factors.get("evidence_mass", 0.0)

    aged = eng.confidence.age_evidence_pass(
        now=time(),
        half_life_s=7 * 86400,
        stale_idle_s=10 * 86400,
    )
    assert aged["experiences_unchanged"] is True
    assert aged["provenance_unchanged"] is True
    assert len(eng.store.experiences) == exp_before
    assert len(eng.store.provenance) == prov_before
    assert concept.evidence_ids == evid_before

    snap2 = eng.confidence.estimate_concept(concept.id)
    mass2 = snap2.factors.get("evidence_mass", 0.0)
    assert mass2 <= mass1 + 1e-9
    stale = eng.confidence.detect_stale(
        "concept", concept.id, now=time(), stale_idle_s=10 * 86400
    )
    assert stale
    assert UncertaintyKind.STALE.value in snap2.uncertainty_kinds or any(
        i.status == EvidenceStatus.STALE for i in stale
    )


def test_reinforcement_restores_influence() -> None:
    eng = CognitiveEngine(agent_id="m5-ev2")
    eng.encode("I prefer step-by-step debugging.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concept = next(c for c in eng.store.concepts.values() if c.evidence_ids)
    now = time()
    for eid in concept.evidence_ids:
        inf = eng.confidence._ensure_influence(
            "concept", concept.id, eid, now=now - 60 * 86400
        )
        inf.weight = 0.2
        inf.last_reinforced = now - 60 * 86400
        inf.status = EvidenceStatus.STALE
        eng.store.evidence_influences[inf.key] = inf
    before = eng.confidence.evidence_weight(
        "concept", concept.id, concept.evidence_ids[0], now=now
    )
    eng.confidence.mark_reinforced(
        "concept", concept.id, concept.evidence_ids, at=now, boost=0.4
    )
    after = eng.confidence.evidence_weight(
        "concept", concept.id, concept.evidence_ids[0], now=now
    )
    assert after > before
    inf = eng.store.evidence_influences[f"concept:{concept.id}:{concept.evidence_ids[0]}"]
    assert inf.status == EvidenceStatus.ACTIVE


def test_sleep_ages_evidence_and_keeps_experiences() -> None:
    eng = CognitiveEngine(agent_id="m5-ev3")
    eng.encode("A beagle is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    dog = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "dog")
    now = time()
    for eid in dog.evidence_ids:
        eng.confidence._ensure_influence("concept", dog.id, eid, now=now - 45 * 86400)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    out = eng.sleep()
    assert "evidence_aging" in out
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n


def test_obsolete_marks_low_influence_not_deletion() -> None:
    eng = CognitiveEngine(agent_id="m5-ev4")
    eng.encode("Obscure fact about widgets.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concept = next(c for c in eng.store.concepts.values() if c.evidence_ids)
    eid = concept.evidence_ids[0]
    now = time()
    inf = eng.confidence._ensure_influence("concept", concept.id, eid, now=now - 100 * 86400)
    inf.weight = 0.06
    inf.last_reinforced = now - 100 * 86400
    eng.store.evidence_influences[inf.key] = inf
    eng.confidence.age_evidence_pass(
        now=now, half_life_s=7 * 86400, stale_idle_s=14 * 86400
    )
    refreshed = eng.store.evidence_influences[inf.key]
    assert refreshed.status in {EvidenceStatus.STALE, EvidenceStatus.OBSOLETE}
    assert eid in concept.evidence_ids
    assert eng.store.experiences.get(eid) is not None
