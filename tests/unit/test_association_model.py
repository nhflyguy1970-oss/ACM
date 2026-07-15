from __future__ import annotations

from acm.associations.model import (
    Association,
    AssociationStage,
    CognitiveDistance,
    RelationKind,
)


def test_distance_bands() -> None:
    strong = Association(
        id="a1",
        source_id="s",
        target_id="t",
        strength_forward=0.9,
        strength_backward=0.4,
        stage=AssociationStage.STRONG,
    )
    assert strong.distance_band() == CognitiveDistance.IMMEDIATE

    near = Association(
        id="a2", source_id="s", target_id="t", strength_forward=0.6, strength_backward=0.5
    )
    assert near.distance_band() == CognitiveDistance.NEAR

    dormant = Association(
        id="a3",
        source_id="s",
        target_id="t",
        strength_forward=0.1,
        stage=AssociationStage.DORMANT,
    )
    assert dormant.distance_band() == CognitiveDistance.DORMANT

    unexpected = Association(
        id="a4",
        source_id="s",
        target_id="t",
        strength_forward=0.5,
        metadata={"unexpected": True},
    )
    assert unexpected.distance_band() == CognitiveDistance.UNEXPECTED


def test_directed_strength_toward() -> None:
    a = Association(
        id="a",
        source_id="dog",
        target_id="animal",
        relation=RelationKind.IS_A_TRAFFIC,
        strength_forward=0.8,
        strength_backward=0.3,
    )
    assert a.strength_toward("dog", "animal") == 0.8
    assert a.strength_toward("animal", "dog") == 0.3
    assert a.weight == 0.8
    assert a.edge_type == RelationKind.IS_A_TRAFFIC


def test_public_dict_has_no_chain_of_thought() -> None:
    a = Association(id="a", source_id="x", target_id="y", relation=RelationKind.RESEMBLES)
    pub = a.to_public()
    assert "reasoning" not in pub
    assert "prompt" not in pub
    assert pub["relation"] == "resembles"
