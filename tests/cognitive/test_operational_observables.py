from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_operational_observables() -> None:
    eng = CognitiveEngine(agent_id="ops")
    eng.encode("Ops observability sample.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    snap = eng.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    assert "storage" in snap and "provenance" in snap and "shadow" in snap
    assert snap["provenance"]["stamps"] >= 1
    blob = str(snap).lower()
    assert "chain of thought" not in blob
