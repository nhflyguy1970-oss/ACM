# Cognitive Abstraction — ACM

**Status:** Architectural for M3  
**Companions:** [`CONCEPT_ARCHITECTURE.md`](CONCEPT_ARCHITECTURE.md) · [`CONCEPT_LIFECYCLE.md`](CONCEPT_LIFECYCLE.md)

## Purpose

Describe how abstraction can *emerge* as cognitive structure.  
**Do not** treat this document as a license to implement reasoning engines in M3.

## How abstraction emerges

1. Multiple Experiences mention related instances (Zeus, Golden Retriever, Labrador).  
2. Shared category language appears (“is a dog”, “dogs at the park”).  
3. Instance Concepts link upward via `is_a` to a category Concept.  
4. Category Concepts may themselves link upward (Dog → Animal) when evidence supports it.  
5. Prototype features of the parent drift toward family resemblance across exemplars.

```
Golden Retriever ──is_a──▶ Dog ──is_a──▶ Animal
Labrador         ──is_a──▶ Dog
Zeus (instance)  ──is_a──▶ Golden Retriever
```

## Generalization & hierarchy

| Mechanism | Support |
|-----------|---------|
| Category induction from “X is a Y” | Seed hierarchy candidates with Experience evidence |
| Sibling reinforcement under shared parent | `resembles` traffic + sibling queries |
| Taxonomy depth | Parent/child/ancestor-safe queries; cycle-blocked |
| Specialization / generalization | ConceptOrgan `specialize` / `generalize_children` |
| Attribute inheritance | Evidence-gated copy of parent attributes only |
| Similarity | Label/feature overlap scores for recognition hints |
| Difference | Distinct attributes / conflicting values remain on children |
| Persistence | `hierarchy_edges` on CognitiveStore snapshots |

See [`CONCEPT_HIERARCHIES.md`](CONCEPT_HIERARCHIES.md) (M5 Cap1).  
See [`MULTI_LEVEL_ABSTRACTION.md`](MULTI_LEVEL_ABSTRACTION.md) (M5 Cap4).

## Prototype formation

As exemplars accumulate, the parent’s **prototype** updates (frequency-weighted features). Children remain specialized. This prepares future recognition (“have I seen something like this?”) without implementing Remembering.

## Future cognitive reasoning (out of scope)

Analogy, inference, and creative synthesis should later consume these structures. M3 only ensures hierarchy, prototypes, exemplars, and similarity hooks exist so reasoning organs will not require redesign.
