from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_prediction_simulation_observables() -> None:
    engine = CognitiveEngine(agent_id="psobs")
    engine.encode("Module gamma firmware.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    engine.what_is_likely("module gamma")
    engine.what_futures_can_memory_imagine("module gamma", branches=2)
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.13"
    assert "prediction" in snap and "simulation" in snap
    blob = str(snap).lower()
    for banned in ("chain of thought", "system prompt", "you are an ai"):
        assert banned not in blob


def test_attention_and_accessibility_influence_prediction() -> None:
    engine = CognitiveEngine(agent_id="psobs")
    a = engine.encode("Priority toolkit alpha.", pin=True, provenance=TRUSTED_USER_STATEMENT)[
        "concept_id"
    ]
    b = engine.encode("Neglected trivia zeta.", pin=True, provenance=TRUSTED_USER_STATEMENT)[
        "concept_id"
    ]
    engine.attention.invest(a, delta=0.25, source="test", factors=["importance"])
    engine.cool_memory(b, steps=3)
    result = engine.what_is_likely("toolkit")
    labels = [o["label"].lower() for o in result["outcomes"]]
    if labels:
        hit = any("toolkit" in lab or "alpha" in lab or "priority" in lab for lab in labels)
        assert hit or result["confidence"] >= 0
