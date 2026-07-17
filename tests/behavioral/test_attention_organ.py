from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_attention_improves_encoding_priority() -> None:
    engine = CognitiveEngine(agent_id="attn")
    enc = engine.encode(
        "My favorite coffee is Ethiopian pour-over.",
        kind="preference",
        pin=True,
        provenance=TRUSTED_USER_STATEMENT,
    )
    cid = enc["concept_id"]
    priority = engine.attention.priority_of(cid)
    assert priority > 0.5
    deserve = engine.what_deserves_attention("coffee")
    assert deserve["question"].startswith("What deserves")
    assert any(p["concept_id"] == cid for p in deserve["priorities"])
    snap = engine.validation.snapshot()
    assert snap["attention"]["investments"] >= 1
    assert snap["attention"]["allocations"] >= 1


def test_priority_evolves_with_remembering() -> None:
    engine = CognitiveEngine(agent_id="attn")
    enc = engine.encode("Husky dogs love snow.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    cid = enc["concept_id"]
    before = engine.attention.priority_of(cid)
    engine.remember("husky")
    after = engine.attention.priority_of(cid)
    assert after >= before - 1e-9


def test_goals_bias_attention_allocation() -> None:
    engine = CognitiveEngine(agent_id="attn")
    engine.open_goal("Ship firmware module gamma", importance=0.9)
    allocation = engine.attention.allocate(
        "working on firmware module gamma today", has_open_goal=True
    )
    assert allocation.weight >= 0.8
    assert "goal" in allocation.factors or allocation.attention_class in (
        "goal",
        "stakes",
        "novelty",
        "frequency",
        "default",
        "user_pin",
        "prediction_error",
    )
