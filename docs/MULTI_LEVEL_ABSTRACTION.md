# Multi-Level Abstraction & General Principles — M5 Cap4

**Status:** Implemented (ACM v0.31.0)  
**Ownership:** Concept organ (D016). Learning applies reversible Adaptations; Prediction audits reinforce/weaken.  
**Invariant:** Abstractions require sufficient Experience evidence. Never invent Experiences. Never rewrite provenance. Principles are probabilistic, never absolute.

## Levels

```
L1 Concrete observations (Experiences)
  → L2 Concepts
  → L3 Generalized concepts (hierarchy + AbstractionRecord)
  → L4 General principles (probabilistic modality)
  → L5 Stable knowledge structures (refined / merged abstractions)
```

Each level retains provenance to supporting concepts and Experiences.

## Pipeline

```
Experiences → Semantic Concepts → Concept Hierarchies (Cap1)
  → Higher-order Abstractions → General Principles
  → Knowledge Structures → Reasoning / Prediction support
```

Prediction Audit (Cap3): hits strengthen supporting abstractions; misses weaken them.

## Models

| Artifact | Role |
|----------|------|
| `AbstractionRecord` | Candidate → active → refined / split / merged / retired |
| `GeneralPrinciple` | `usually` / `tends` / `commonly` / `rarely` — never absolute |

## Lifecycle

| Operation | Behavior |
|-----------|----------|
| Propose | Rejected without ≥ min evidence Experiences |
| Promote | Candidate → active |
| Refine | Add concepts/evidence; bump confidence |
| Split / Merge | Preserve history on source records |
| Retire | Closed but queryable |
| Reinforce | Cap3 audit / explicit strengthen|weaken |

## Explainability

`explain_abstraction` answers why it exists, supporting concepts/experiences, conflicts, confidence change, and revisability.

## Non-goals

- No invented category labels from clustering alone
- No Experience rewrite
- No absolute truths
- Cap5: [`TEMPORAL_PATTERNS.md`](TEMPORAL_PATTERNS.md)
+ Cap5: [`TEMPORAL_PATTERNS.md`](TEMPORAL_PATTERNS.md)

## Certification

- Behavioral: `tests/behavioral/test_m5_multi_level_abstraction.py`
- Learning: `tests/cognitive/test_m5_abstraction_learning_cert.py` (L17–L18)
