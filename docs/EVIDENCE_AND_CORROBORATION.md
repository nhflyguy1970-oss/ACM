# Evidence and Corroboration — ACM

**Status:** Canonical companion for M15/M16  
**Companions:** [`MEMORY_RECONCILIATION.md`](MEMORY_RECONCILIATION.md) · [`CONFIDENCE_MODEL.md`](CONFIDENCE_MODEL.md) · [`HUMAN_MEMORY_CONFLICTS.md`](HUMAN_MEMORY_CONFLICTS.md)

## Biological function

Evidence accumulates as episodes. Corroboration is repeated, consistent evidence that raises confidence. Conflict is inconsistent evidence that lowers confidence or forces context dependence. Neither deletes the past.

## Technical function

| Signal | ACM source | Effect |
|--------|------------|--------|
| Multi-evidence Concepts | `Concept.evidence_ids` | Supports `reinforce` |
| Reflective consistency | Reflective Experience outcomes | Supports |
| `conflicts_with` Associations | Association organ | Conflict / competing |
| Attribute contest | High + low confidence attributes | Conflict |
| Prediction dispersion | Prediction outcomes | Conflict or support |

Reconciliation creates a **new** `ReconciliationRecord`. Confidence organ recalibrates living Concept confidence and records `ConfidenceEvent`s.

## Ownership

- Reconciliation owns conflict/corroboration classification and lineage.
- Confidence owns numeric evolution.
- Experiences remain immutable evidence forever.

## Intentional omissions

External fact-checkers; majority-vote truth without lineage; automatic Experience deletion under conflict.
