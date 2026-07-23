# Learning Explainability — M5 Cap6

**Status:** Implemented (ACM v0.33.0)  
**Ownership:** Learning organ (`explain_learning` / `why_was_this_learned`).  
**Invariant:** Public explanations only. Provenance preserved. Never invents Experiences. Never exposes implementation internals.

## Surfaces

| Question | Field / API |
|----------|-------------|
| Why does this exist? | `why_exists` / `answer` |
| Supporting / conflicting evidence | `supporting_evidence`, `conflicting_evidence` |
| Confidence history | `confidence_history` |
| Abstraction / prediction / hypothesis history | dedicated history fields |
| Temporal pattern influence | `temporal_pattern_influence` |
| Adoption / reflection / consolidation | corresponding `*_influence` / `*_history` |
| Reversible? | `reversible`, `why_reversible` |

## Non-goals

- No CoT dumps, file paths, class names, or organ internals in answers
- Cap7 stability: [`LEARNING_STABILITY.md`](LEARNING_STABILITY.md)

## Certification

- Behavioral: `tests/behavioral/test_m5_learning_explainability.py`
- Learning: `tests/cognitive/test_m5_learning_explainability_cert.py` (L21–L22)
