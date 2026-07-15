# Cognitive Ownership

**Status:** Normative (v0.16.0)  
**Schema:** `cognitive_ownership.v1`

## Rule

Every cognitive question has **exactly one primary cognitive owner**.

Supporting organs may contribute evidence. The language model is never an owner.

## Ownership object

| Field | Meaning |
|-------|---------|
| `intent` | Classified `CognitiveIntent` |
| `primary_organ` | Sole owner (`identity`, `remembering`, `learning`, …) |
| `supporting_organs` | Optional contributors |
| `uncertain` | Classification uncertainty flag |
| `confidence` | Classification confidence |
| `rationale` | Human-readable ownership reason |

## Organ vocabulary

| Organ | Responsibility |
|-------|----------------|
| `identity` | Assistant / user identity schemas |
| `remembering` | Episodic / autobiographical reconstruction |
| `experiences` | Experience evidence support |
| `concepts` | Conceptual structure |
| `associations` | Relational structure |
| `learning` | Adaptation / lessons |
| `reflection` | Metacognitive thought |
| `confidence` | Certainty assessment |
| `reconciliation` | Conflict handling |
| `goals` | Active goal retrieval |
| `working_memory` | Working buffer / residue |
| `context` | Context frame |
| `none` | Non-cognitive — host execution |

## Prohibitions

- Language model selecting the organ
- Host bypassing ownership for cognitive intents
- Dual primary owners
- Silent reassignment of uncertain cognitive questions to LM generation
