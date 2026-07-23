"""M5 Cap5 learning certification — temporal patterns (L19–L20)."""

from __future__ import annotations

from time import time

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l19_temporal_patterns_evidence_based_never_invent() -> None:
    eng = CognitiveEngine(agent_id="m5-l19")
    eng.encode("I usually drink coffee after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("I usually drink coffee after breakfast.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    exp_n = len(eng.store.experiences)
    prov_n = len(eng.store.provenance)
    ids = list(eng.store.experiences.keys())
    eng.learning.observe_temporal_pattern(
        antecedent="breakfast",
        consequent="coffee",
        experience_id=ids[0],
        period_hint="morning",
    )
    eng.learning.observe_temporal_pattern(
        antecedent="breakfast",
        consequent="coffee",
        experience_id=ids[-1],
        period_hint="morning",
    )
    assert len(eng.store.experiences) == exp_n
    assert len(eng.store.provenance) == prov_n
    e1 = eng.explain_temporal_pattern("coffee")
    e2 = eng.explain_temporal_pattern("coffee")
    assert e1["answer"] == e2["answer"]
    assert e1["invents_experiences"] is False
    # Reject unknown experience id
    bad = eng.learning.observe_temporal_pattern(
        antecedent="x", consequent="y", experience_id="exp_missing"
    )
    assert bad["status"] == "rejected"


def test_l20_inactive_patterns_weaken_reproducibly() -> None:
    eng = CognitiveEngine(agent_id="m5-l20")
    eng.encode("Saturdays I go fishing.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eid = next(iter(eng.store.experiences))
    eng.learning.observe_temporal_pattern(
        antecedent="Saturday",
        consequent="fishing",
        experience_id=eid,
        period_hint="saturday",
        kind="routine",
    )
    pat = next(iter(eng.store.temporal_patterns.values()))
    pat.last_observed = time() - 30 * 86400
    before = pat.confidence
    a1 = eng.age_temporal_patterns(now=time(), weaken_idle_s=14 * 86400)
    after = eng.store.temporal_patterns[pat.id].confidence
    assert after <= before + 1e-9
    assert a1["experiences_unchanged"] is True
    # Fresh engine same aging class
    eng2 = CognitiveEngine(agent_id="m5-l20b")
    eng2.encode("Saturdays I go fishing.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eid2 = next(iter(eng2.store.experiences))
    eng2.learning.observe_temporal_pattern(
        antecedent="Saturday",
        consequent="fishing",
        experience_id=eid2,
        period_hint="saturday",
        kind="routine",
    )
    p2 = next(iter(eng2.store.temporal_patterns.values()))
    p2.last_observed = time() - 30 * 86400
    a2 = eng2.age_temporal_patterns(now=time(), weaken_idle_s=14 * 86400)
    assert a2["weakened"] + a2["dormant"] + a2["retired"] >= 1
