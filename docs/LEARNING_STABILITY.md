# Learning Stability — M5 Cap7

**Status:** Implemented (ACM v0.34.0)  
**Backlog:** B59  
**Invariant:** Learning may reorganize living structure but must **never invent** Experiences or rewrite Experience history. Provenance preserved.

## Purpose

Long-duration learning must remain bounded and reproducible after months or years of simulated operation: confidence stays in range, structures do not explode, consolidation is deterministic given state, and recursive re-learning from the same Reflective Experience is blocked.

## Public APIs

| API | Role |
|-----|------|
| `check_learning_stability()` | Read-only report: growth vs limits, confidence breaches, oscillation |
| `enforce_learning_stability()` | Clamp confidence to `[min, max]`; cool excess adaptations / patterns / hypotheses metadata; never deletes Experiences |

`sleep()` / `consolidate()` invokes enforcement after aging passes.

## Guarantees

- **Bounded confidence** — concept adaptations clamp to `LearningStabilityLimits` (`0.05`–`0.98` by default)
- **No recursive learning** — a Reflective Experience that already produced applied Adaptations is not re-learned
- **No temporal-pattern explosion** — new patterns rejected at hard cap; excess retired on enforce
- **Bounded growth** — report breaches for concepts, adaptations, abstractions, hypotheses, audits, patterns
- **Deterministic replay** — same store + cues → same stability report fields for growth / breaches
- **No invented Experiences** — enforce asserts Experience and provenance counts unchanged
- **No internals leakage** — public payloads set `exposes_internals=False`

## Limits (defaults)

See `acm/learning/stability.py` → `LearningStabilityLimits`.

## Related

- Cap6 explainability: [`LEARNING_EXPLAINABILITY.md`](LEARNING_EXPLAINABILITY.md)
- Certification gates L23–L24 in [`LEARNING_CERTIFICATION.md`](LEARNING_CERTIFICATION.md)
