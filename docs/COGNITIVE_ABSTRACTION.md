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

| Mechanism | M3 support |
|-----------|------------|
| Category induction from “X is a Y” | Seed hierarchy candidates |
| Sibling reinforcement under shared parent | Strengthens parent nucleus |
| Taxonomy depth | Parent/child queries; no inference engine |
| Similarity | Label/feature overlap scores for recognition hints |
| Difference | Distinct attributes / conflicting values remain on children |

## Prototype formation

As exemplars accumulate, the parent’s **prototype** updates (frequency-weighted features). Children remain specialized. This prepares future recognition (“have I seen something like this?”) without implementing Remembering.

## Future cognitive reasoning (out of scope)

Analogy, inference, and creative synthesis should later consume these structures. M3 only ensures hierarchy, prototypes, exemplars, and similarity hooks exist so reasoning organs will not require redesign.
