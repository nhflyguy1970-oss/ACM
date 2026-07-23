"""M5 Cap1 learning certification — hierarchy is evidence-based and never invents memory."""

from __future__ import annotations

from acm import CognitiveEngine
from acm.provenance import TRUSTED_USER_STATEMENT


def test_l11_hierarchy_requires_evidence_and_no_invented_experiences() -> None:
    eng = CognitiveEngine(agent_id="m5-l11")
    before = len(eng.store.experiences)
    first = eng.encode("A collie is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    eng.encode("A husky is a dog.", pin=True, provenance=TRUSTED_USER_STATEMENT)
    after_encode = len(eng.store.experiences)
    assert after_encode == before + 2

    hier = eng.concept_hierarchy("collie")
    assert hier["known"] is True
    assert hier["evidence_ids"]

    dog = next(c for c in eng.store.concepts.values() if c.labels and c.labels[0] == "dog")
    prior_id = first["experience_id"]
    reflective = eng.experiences.reflect(
        prior_id,
        "Pattern: multiple dog breeds share the dog category.",
        concept_ids=tuple(list(dog.child_ids)[:2] + [dog.id]),
        metadata={"outcomes": "pattern"},
    )
    exp_count = len(eng.store.experiences)
    eng.learning.learn_from_reflection(reflective.id)
    assert len(eng.store.experiences) == exp_count
    # Every hierarchy edge remains Experience-linked or empty only if rebuilt without stamp —
    # Cap1 encode path must leave evidence on dog-breed edges.
    breed_edges = [
        e
        for e in eng.store.hierarchy_edges.values()
        if e.parent_id == dog.id
    ]
    assert breed_edges
    assert all(e.evidence_ids for e in breed_edges)


def test_l12_hierarchy_explainable_and_deterministic() -> None:
    eng = CognitiveEngine(agent_id="m5-l12")
    for text in (
        "A maple is a tree.",
        "An oak is a tree.",
        "A pine is a tree.",
    ):
        eng.encode(text, pin=True, provenance=TRUSTED_USER_STATEMENT)

    a = eng.concept_hierarchy("maple")
    b = eng.concept_hierarchy("maple")
    assert a["answer"] == b["answer"]
    assert a["parents"] == b["parents"]
    assert set(a["evidence_ids"]) == set(b["evidence_ids"])
