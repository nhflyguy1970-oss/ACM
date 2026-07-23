# Temporal Pattern Recognition — M5 Cap5

**Status:** Implemented (ACM v0.32.0)  
**Ownership:** Learning organ (TemporalPattern records). Sleep ages unobserved patterns. Prediction may boost from active patterns.  
**Invariant:** Patterns require Experience evidence. Unobserved patterns weaken. Experiences/provenance never deleted.

## Supports

| Kind | Examples |
|------|----------|
| routine / habit | Saturday fishing; coffee after breakfast |
| schedule | morning productivity |
| seasonal | winter/summer cues |
| recurring / periodic | weekly / daily hints |
| trend | confidence/strength evolution via observation vs aging |

## Lifecycle

```
Observe Experience → TemporalPattern (formed/reinforced)
  → Sleep / age_temporal_patterns (idle → weakening → dormant → retired)
  → Prediction may consume active patterns
```

## APIs

- `observe_temporal_pattern` / encode predictive hook
- `list_temporal_patterns` / `explain_temporal_pattern`
- `age_temporal_patterns` (also during `sleep`)
- `discover_patterns_from_predictive_experiences`

## Non-goals

- No invented Experiences
- No absolute schedules
- Cap6+ explainability / stability: [`LEARNING_EXPLAINABILITY.md`](LEARNING_EXPLAINABILITY.md), [`LEARNING_STABILITY.md`](LEARNING_STABILITY.md)

## Certification

- Behavioral: `tests/behavioral/test_m5_temporal_patterns.py`
- Learning: `tests/cognitive/test_m5_temporal_pattern_learning_cert.py` (L19–L20)
- Long-duration: `tests/performance/test_m5_temporal_long_duration.py`
