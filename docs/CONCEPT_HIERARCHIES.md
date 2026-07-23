# Concept Hierarchies — M5 Cap1

**Status:** Implemented (ACM v0.28.0)  
**Ownership:** Concept organ (D016) — Associations mirror `is_a_traffic` / `resembles` only  
**Invariant:** Hierarchy creation is evidence-based. Learning never invents Experiences.

## Capabilities

| Feature | Behavior |
|---------|----------|
| Parent / child | `Concept.parent_ids` / `child_ids` + persisted `HierarchyEdge` |
| Sibling | Children sharing a parent; `siblings()` / `what_is_this` hierarchy block |
| Inherited relationships | `inherit_attributes` copies **existing** parent attributes only |
| Clustering | `propose_hierarchy_from_clusters` → pending proposals (no invented parents) |
| Specialization | `specialize()` / `HierarchyKind.SPECIALIZES` |
| Generalization | `generalize_children()` under an **existing** parent |
| Evidence | Edges carry `evidence_ids`; encode bind stamps Experiences |
| Explainability | `explain_hierarchy` / `engine.concept_hierarchy` |
| Persistence | `store.hierarchy_edges` in snapshot codec |
| Cycle safety | `link_is_a` refuses ancestor↔descendant inversion |

## Learning & Sleep

- Learning `GENERALIZE` on reflective `pattern` may reinforce evidenced `is_a` links and soft-inherit attributes via Concept organ.
- Sleep may emit `hierarchy_candidate:…` strings for host assent; does not auto-mint Concepts.

## Non-goals

- No parallel ontology service
- No taxonomy ownership move to Associations
- No fabricated category labels from clusters
- No Experience rewrites

## Certification

- Behavioral: `tests/behavioral/test_m5_concept_hierarchies.py`
- Learning: `tests/cognitive/test_m5_hierarchy_learning_cert.py` (L11–L12)
- Full gates: pytest `tests/` + learning certification runner
