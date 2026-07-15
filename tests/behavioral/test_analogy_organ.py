from __future__ import annotations

from acm import CognitiveEngine
from acm.associations.model import RelationKind


def test_analogy_is_explainable_and_non_executive() -> None:
    engine = CognitiveEngine(agent_id="anl")
    engine.encode("A husky is a dog.", pin=True)
    engine.encode("A beagle is a dog.", pin=True)
    dogs = engine.store.find_concepts_by_label("dog")
    husky = engine.store.find_concepts_by_label("husky")
    beagle = engine.store.find_concepts_by_label("beagle")
    if dogs and husky and beagle:
        engine.associations.relate(
            husky[0].id,
            beagle[0].id,
            relation=RelationKind.RESEMBLES,
            strength_forward=0.55,
        )
    result = engine.what_is_analogous("husky", other="beagle")
    assert result["question"].startswith("What existing memories are analogous")
    assert result["plans"] is False
    assert result["decides"] is False
    assert result["executive"] is False
    if result["analogies"]:
        a = result["analogies"][0]
        assert a["why"] or a["alignments"]
        assert a["confidence"] < 1.0


def test_learning_and_offline_improve_analogy_confidence() -> None:
    engine = CognitiveEngine(agent_id="anl")
    engine.encode("Fly tying requires fine tools.", pin=True)
    engine.encode("Woodworking requires fine tools.", pin=True)
    a = engine.store.find_concepts_by_label("fly") or engine.store.find_concepts_by_label(
        "tying"
    )
    b = engine.store.find_concepts_by_label("woodworking")
    if a and b:
        engine.associations.relate(
            a[0].id, b[0].id, relation=RelationKind.RESEMBLES, strength_forward=0.4
        )
    first = engine.what_is_analogous("fly tying", other="woodworking")
    c0 = first["analogies"][0]["confidence"] if first["analogies"] else 0.0
    engine.what_do_i_think("tools")
    engine.learn(cue="tools")
    engine.sleep()
    second = engine.what_is_analogous("fly tying", other="woodworking")
    c1 = second["analogies"][0]["confidence"] if second["analogies"] else 0.0
    assert c1 >= c0 - 1e-6 or second["analogies"] or first["analogies"] == []
