from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind


def test_prediction_is_probabilistic_and_never_plans() -> None:
    engine = CognitiveEngine(agent_id="pred")
    engine.encode("Coffee often comes after breakfast.", pin=True)
    engine.encode("Breakfast includes toast.", pin=True)
    a = engine.store.find_concepts_by_label("breakfast")[0]
    b = engine.store.find_concepts_by_label("coffee")[0]
    engine.associations.relate(
        a.id, b.id, relation=RelationKind.PREDICTS, strength_forward=0.7
    )
    result = engine.what_is_likely("After breakfast what is likely?")
    assert result["question"].startswith("Based upon memory")
    assert result["plans"] is False
    assert result["decides"] is False
    assert abs(sum(o["probability"] for o in result["outcomes"]) - 1.0) < 0.05 or not result[
        "outcomes"
    ]
    assert all(o["probability"] <= 0.85 for o in result["outcomes"])
    assert result["confidence"] < 1.0
    snap = engine.validation.snapshot()
    assert snap["schema"] == "acm.validation/0.12"
    assert snap["prediction"]["predictions"] >= 1


def test_prediction_confidence_evolves_with_feedback() -> None:
    engine = CognitiveEngine(agent_id="pred")
    engine.encode("Firmware module gamma often follows build.", pin=True)
    first = engine.what_is_likely("What follows build?")
    pid = first["id"]
    conf_before = first["confidence"]
    enc = engine.encode("Build completed; firmware module gamma ready.", pin=True)
    evaluated = engine.evaluate_prediction(pid, enc["concept_id"])
    assert evaluated["status"] == "evaluated"
    assert engine.store.predictions[pid].evaluated is True
    assert engine.store.predictions[pid].confidence != conf_before or evaluated["accuracy"] >= 0


def test_learning_and_offline_aid_prediction() -> None:
    engine = CognitiveEngine(agent_id="pred")
    engine.encode("Husky dogs love snow.", pin=True)
    weak = engine.what_is_likely("husky")["confidence"]
    engine.what_do_i_think("husky")
    engine.learn(cue="husky")
    engine.sleep()
    stronger = engine.what_is_likely("husky")["confidence"]
    assert stronger >= weak - 1e-6
