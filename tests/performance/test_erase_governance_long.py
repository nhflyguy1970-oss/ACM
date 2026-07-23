"""B36 long-duration — repeated forget/assent cycles remain stable."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_long_duration_erase_governance_stable() -> None:
    eng = CognitiveEngine(agent_id="b36-long")
    cities = ["Boston", "Chicago", "Denver", "Austin", "Seattle"]
    for city in cities:
        eng.encode(f"I live in {city}.", pin=True, provenance=TRUSTED_USER_STATEMENT)
        out = eng.apply_erase_request("Forget my old address.")
        assert out["status"] == "applied"
        assert out["experiences_deleted"] is False
        eng.sleep()
    # All Experiences retained
    assert len(eng.store.experiences) >= len(cities)
    # No active location after final forget
    user = eng.identity.schema_concept("user")
    assert not any(a.active and a.key == "location" for a in user.attributes)
