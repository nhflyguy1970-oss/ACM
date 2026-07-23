"""M5 Cap5 long-duration stress — many observations, aging, no runaway."""

from __future__ import annotations

from time import time

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_temporal_patterns_bounded() -> None:
    eng = CognitiveEngine(agent_id="m5-c5-long")
    # Simulate repeated habit observations across "months"
    base = time() - 180 * 86400
    for i in range(40):
        eng.encode(
            f"Autobiographical note {i}: breakfast then coffee.",
            pin=True,
            provenance=TRUSTED_USER_STATEMENT,
        )
        eid = list(eng.store.experiences.keys())[-1]
        # Stagger observation times — single pattern key
        eng.learning.observe_temporal_pattern(
            antecedent="breakfast",
            consequent="coffee",
            experience_id=eid,
            period_hint="morning",
            kind="habit",
            now=base + i * 3 * 86400,
        )
    assert len(eng.store.temporal_patterns) == 1
    pat = next(iter(eng.store.temporal_patterns.values()))
    assert pat.observation_count >= 40
    assert 0.05 <= pat.confidence <= 0.95
    peak = pat.confidence
    # Long idle then age → weaken, still single pattern (no explosion)
    pat.last_observed = time() - 60 * 86400
    for _ in range(5):
        eng.age_temporal_patterns(now=time(), weaken_idle_s=14 * 86400)
        eng.sleep()
    assert len(eng.store.temporal_patterns) == 1
    assert eng.store.temporal_patterns[pat.id].confidence <= peak + 1e-9
    assert 0.05 <= eng.store.temporal_patterns[pat.id].confidence <= 0.95
    # Experience count only grew from encodes — aging invents nothing
    assert len(eng.store.experiences) == 40
