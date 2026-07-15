# Uncertainty Model — ACM

**Status:** Canonical for M16 (implemented)  
**Companions:** [`CONFIDENCE_MODEL.md`](CONFIDENCE_MODEL.md) · [`MEMORY_RECONCILIATION.md`](MEMORY_RECONCILIATION.md)

## Cognitive role

Uncertainty is the complement of confidence: named kinds of not-knowing attached to living memory. It is owned by the Confidence organ as taxonomy + reporting — not a second organ and not executive risk management.

## Uncertainty kinds

| Kind | Meaning |
|------|---------|
| `known_unknown` | Trace is sparse or poorly accessible |
| `evidence` | Too few Experiences corroborate |
| `prediction` | Prospective memory is diffuse / low confidence |
| `simulation` | Hypothetical future is marked uncertain by nature |
| `learning` | Provisional / recently adapted structures |
| `reflection` | Reflective Experience flagged contradiction or uncertainty |

## Biological function

Organisms distinguish *not knowing that* from *doubt about that*. Labeling uncertainty shapes retrieval caution — still a memory function.

## Technical function

- Emitted on `ConfidenceSnapshot.uncertainty_kinds`
- Aggregated via `ConfidenceOrgan.global_uncertainty()`
- Observed in validation snapshot under `confidence` + assessment public payload
- Never removes evidence; never plans

## Intentional omissions

Monte-Carlo dropout; formal epistemic logic; world-model aleatoric vs epistemic solvers beyond memory-facing labels.
