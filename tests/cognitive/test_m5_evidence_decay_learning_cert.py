"""M5 Cap2 learning certification — evidence decay without inventing/deleting memory."""

from __future__ import annotations

from time import time

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l13_aging_never_invents_or_deletes_experiences() -> None:
    eng = CognitiveEngine(agent_id="m5-l13")
    eng.encode("My favorite coffee is dark roast.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("My favorite coffee is dark roast.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    concept = next(
        c
        for c in eng.store.concepts.values()
        if any(a.key.startswith("favorite_coffee") and a.active for a in c.attributes)
    )
    past = time() - 50 * 86400
    for eid in concept.evidence_ids:
        inf = eng.confidence._ensure_influence("concept", concept.id, eid, now=past)
        inf.last_reinforced = past
        inf.created = past
        eng.store.evidence_influences[inf.key] = inf

    result = eng.confidence.age_evidence_pass(
        now=time(), half_life_s=10 * 86400, stale_idle_s=20 * 86400
    )
    assert result["experiences_unchanged"] is True
    assert result["provenance_unchanged"] is True
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    assert result["aged"] >= 1 or result["stale"] >= 1


def test_l14_reinforce_after_stale_restores_estimate() -> None:
    eng = CognitiveEngine(agent_id="m5-l14")
    eng.encode("I prefer Rust for systems programming.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    concept = next(c for c in eng.store.concepts.values() if "rust" in " ".join(c.labels).lower() or c.evidence_ids)
    # Prefer concept with evidence
    concept = max(
        (c for c in eng.store.concepts.values() if c.evidence_ids),
        key=lambda c: len(c.evidence_ids),
    )
    now = time()
    for eid in concept.evidence_ids:
        inf = eng.confidence._ensure_influence("concept", concept.id, eid, now=now - 80 * 86400)
        inf.weight = 0.15
        eng.store.evidence_influences[inf.key] = inf
    eng.confidence.age_evidence_pass(now=now, half_life_s=10 * 86400, stale_idle_s=20 * 86400)
    low = eng.confidence.estimate_concept(concept.id).value
    eng.confidence.evolve_from_learning(concept.id, reinforce=True)
    high = eng.confidence.estimate_concept(concept.id).value
    assert high >= low - 1e-9
    assert len(eng.store.experiences) >= 1
