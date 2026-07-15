# Confidence Model — ACM

**Status:** Canonical for M16 (implemented)  
**Cognitive question:** *How certain am I that this memory is accurate?*  
**Companions:** [`UNCERTAINTY_MODEL.md`](UNCERTAINTY_MODEL.md) · [`EVIDENCE_AND_CORROBORATION.md`](EVIDENCE_AND_CORROBORATION.md) · [`MEMORY_RECONCILIATION.md`](MEMORY_RECONCILIATION.md)

## Human memory reality check

| # | Question | Answer |
|---|----------|--------|
| 1 | Exists in human cognitive memory? | Yes — feeling-of-knowing / memory confidence evolves with evidence |
| 2 | Memory process (not executive)? | Yes — estimates accuracy of memory, does not select actions |
| 3 | Models function not mechanism? | Yes — evolvable confidence scalars + events |
| 4 | ACM ≠ Aria boundary? | Yes |
| 5 | More human-like memory? | Yes — confidence is dynamic, explainable, never static |

## Scientific foundations

| Grade | Finding |
|-------|---------|
| **Well-supported** | Metamemory confidence tracks cue familiarity, corroboration, and conflict; confidence is calibratable |
| **Emerging** | Cross-domain confidence transfer rules |
| **Speculation** | Exact numeric mapping of neural confidence |

## Biological function

Confidence lets organisms act on memory without treating every trace as equally certain. It rises with corroboration and successful reuse; it falls with conflict, sparsity, and reflective doubt — without erasing experience.

## Technical function

| Field | Content |
|-------|---------|
| Organ | `ConfidenceOrgan` |
| Public API | `CognitiveEngine.how_certain_am_i(cue=, concept_id=)` |
| Verb | `MemoryVerb.ASSESS` |
| Owns | Estimation, evolution, inheritance/propagation via living Concept confidence, recalibration from Reconciliation |
| Artifacts | `ConfidenceSnapshot`, `ConfidenceEvent` |
| Sources of evolution | Experience encode · Learning · Reconciliation corroboration/conflict · Accessibility · Priority · Identity sparsity |
| Validation | `acm.validation/0.12` → `confidence` aggregate + legacy `confidence_deltas` |

## Ownership

| Owns | Does not own |
|------|----------------|
| Confidence policy & evolution | Reconciliation lineage (M15) |
| Uncertainty tagging on estimates | Planning thresholds / decisions |
| Auditable confidence events | Rewriting Experience history |

## Intentional omissions

Bayesian belief networks as a hard requirement; personality-trait “self-esteem”; action policies based on confidence thresholds (executive / Aria).
