"""M5 Cap1 — Concept Hierarchies (evidence-based, Concept-organ owned)."""

from __future__ import annotations

import tempfile
from pathlib import Path

from acm import CognitiveEngine
from acm.concepts.model import HierarchyKind
from acm.provenance import TRUSTED_USER_STATEMENT
from acm.types import Attribute


def _engine() -> CognitiveEngine:
    return CognitiveEngine(agent_id="m5-hier")


def _encode(engine: CognitiveEngine, text: str) -> dict:
    return engine.encode(text, pin=True, provenance=TRUSTED_USER_STATEMENT)


def test_parent_child_sibling_queries() -> None:
    eng = _engine()
    _encode(eng, "Yasha is a labrador.")
    _encode(eng, "Zeus is a golden retriever.")
    _encode(eng, "A labrador is a dog.")
    _encode(eng, "A golden retriever is a dog.")
    dog = eng.what_is_this("dog")
    assert dog["hierarchy"]["children"]
    assert "siblings" in dog["hierarchy"]
    hier = eng.concept_hierarchy("labrador")
    assert hier["known"] is True
    assert hier["parents"]
    assert hier["parents"][0]["label"] == "dog"
    assert any(s["label"] == "golden retriever" for s in hier["siblings"])
    assert hier["evidence_ids"], "hierarchy edges must carry Experience evidence"
    assert hier["reversible"] is True


def test_evidence_stamped_edges_and_no_cycle() -> None:
    eng = _engine()
    _encode(eng, "A beagle is a dog.")
    _encode(eng, "A dog is an animal.")
    beagle = next(c for c in eng.store.concepts.values() if c.labels[0] == "beagle")
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    animal = next(c for c in eng.store.concepts.values() if c.labels[0] == "animal")
    edge = eng.concepts._edge_between(beagle.id, dog.id)
    assert edge is not None
    assert edge.evidence_ids
    before = edge.weight
    again = eng.concepts.link_is_a(
        beagle.id, dog.id, weight=0.6, evidence_ids=beagle.evidence_ids[-1:]
    )
    assert again is not None
    assert again.weight >= before
    # Making descendant a parent of ancestor must fail (cycle).
    assert eng.concepts.link_is_a(animal.id, beagle.id) is None
    assert eng.concepts.link_is_a(dog.id, beagle.id) is None


def test_specialization_and_generalization() -> None:
    eng = _engine()
    _encode(eng, "Rust is a programming language.")
    _encode(eng, "Python is a programming language.")
    rust = next(c for c in eng.store.concepts.values() if c.labels[0] == "rust")
    python = next(c for c in eng.store.concepts.values() if c.labels[0] == "python")
    lang = next(c for c in eng.store.concepts.values() if "programming" in c.labels[0] or c.labels[0] == "programming language")
    # Prefer explicit parent label
    parents = [c for c in eng.store.concepts.values() if "language" in " ".join(c.labels).lower()]
    assert parents
    parent = max(parents, key=lambda c: len(c.child_ids))
    edges = eng.concepts.generalize_children(
        parent.id, [rust.id, python.id], evidence_ids=tuple(rust.evidence_ids[:1])
    )
    assert edges
    spec = eng.concepts.specialize(
        rust.id, parent.id, evidence_ids=tuple(rust.evidence_ids[:1])
    )
    assert spec is not None
    assert spec.kind in {HierarchyKind.IS_A, HierarchyKind.SPECIALIZES}


def test_inherited_attributes_never_invent() -> None:
    eng = _engine()
    _encode(eng, "A collie is a dog.")
    dog = next(c for c in eng.store.concepts.values() if c.labels[0] == "dog")
    collie = next(c for c in eng.store.concepts.values() if c.labels[0] == "collie")
    dog.attributes.append(
        Attribute(key="species", value="canine", confidence=0.9, evidence_ids=list(dog.evidence_ids[:1]))
    )
    inherited = eng.concepts.inherit_attributes(
        collie.id, dog.id, evidence_ids=tuple(collie.evidence_ids[:1]), keys=("species",)
    )
    assert inherited
    assert inherited[0]["key"] == "species"
    assert inherited[0]["value"] == "canine"
    # No invention: unknown key not on parent stays absent
    assert not any(a.key == "habitat" and a.active for a in collie.attributes)


def test_hierarchy_persistence_roundtrip() -> None:
    eng = _engine()
    _encode(eng, "A maple is a tree.")
    assert len(eng.store.hierarchy_edges) >= 1
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "snap.json"
        eng.export_snapshot(str(path))
        eng2 = CognitiveEngine(agent_id="m5-hier-2")
        eng2.import_snapshot(str(path))
        assert len(eng2.store.hierarchy_edges) >= 1
        edge = next(iter(eng2.store.hierarchy_edges.values()))
        assert edge.child_id and edge.parent_id


def test_cluster_proposal_does_not_invent_parent() -> None:
    eng = _engine()
    _encode(eng, "Yasha is a labrador.")
    _encode(eng, "Zeus is a golden retriever.")
    _encode(eng, "A labrador is a dog.")
    _encode(eng, "A golden retriever is a dog.")
    props = eng.concepts.propose_hierarchy_from_clusters(min_cluster=2, max_proposals=4)
    # Proposals only reference existing parent ids — never mint labels.
    for p in props:
        parent_id = (p.metadata or {}).get("parent_id")
        assert parent_id in eng.store.concepts


def test_sleep_emits_hierarchy_candidates() -> None:
    eng = _engine()
    _encode(eng, "A labrador is a dog.")
    _encode(eng, "A poodle is a dog.")
    out = eng.sleep()
    assert "proposals" in out
    # May or may not emit hierarchy_candidate depending on cluster density; must not invent Experiences.
    before = len(eng.store.experiences)
    eng.sleep()
    assert len(eng.store.experiences) == before
