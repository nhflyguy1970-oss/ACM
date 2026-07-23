# Counterfactual Reasoning & Prediction Audit — M5 Cap3

**Status:** Implemented (ACM v0.30.0)  
**Ownership:** Prediction organ (hypotheses + audits). Learning applies reversible Adaptations only.  
**Invariant:** Audits are append-only. Hypotheses close but remain accessible. Experiences and provenance are never rewritten or invented.

## Pipeline

```
Prediction
  → Observed Outcome
  → Comparison (hit | partial | miss)
  → Calibration (prediction confidence)
  → Confidence Update (Cap2 influence / living confidence)
  → Learning (Adaptations citing audit evidence)
```

## Models

| Artifact | Role |
|----------|------|
| `Hypothesis` | Competing claim with lifecycle: active → disproved / superseded / withdrawn |
| `PredictionAudit` | Permanent comparison + calibration + explanation trail |

## Explanation surfaces

| Question | API |
|----------|-----|
| Why do you believe this? | `explain_belief_change` |
| What evidence supports / disagrees? | supporting / conflicting fields |
| What changed your mind? / When? | `what_changed`, `when_confidence_changed` |
| Alternatives / rejected? | `competing_hypotheses`, `rejected_hypotheses` |
| What would raise/lower confidence? | listed heuristics (evidence reinforce / contradiction / Cap2 aging) |

## Non-goals

- No Experience invention or rewrite
- No provenance mutation
- No planning / decision making

Cap4 multi-level abstractions consume audit outcomes:
[`MULTI_LEVEL_ABSTRACTION.md`](MULTI_LEVEL_ABSTRACTION.md).

## Certification

- Behavioral: `tests/behavioral/test_m5_prediction_audit.py`
- Learning: `tests/cognitive/test_m5_prediction_audit_learning_cert.py` (L15–L16)
- Gates: full `pytest tests/` + `scripts/acm_learning_certification.py`
