# Evidence Weighting & Decay — M5 Cap2

**Status:** Implemented (ACM v0.29.0)  
**Ownership:** Confidence organ (influence/certainty). Forgetting remains accessibility-only.  
**Invariant:** Aging lowers influence. Provenance, `evidence_ids`, and Experiences are never deleted by Cap2.

## Model

`EvidenceInfluence` records per `(target_kind, target_id, experience_id)`:

| Field | Meaning |
|-------|---------|
| `weight` | Current influence ∈ [floor, 1] |
| `last_reinforced` | Last refresh timestamp |
| `status` | `active` \| `stale` \| `obsolete` |

## Behaviors

| Capability | Mechanism |
|------------|-----------|
| Accumulation | Encode/learning reinforce bumps living confidence + refreshes weights |
| Aging / decay | `age_evidence_pass` (host via `sleep`) exponentially softens unreinformed weights |
| Reinforcement | `mark_reinforced` / `evolve_from_learning(reinforce=True)` restores weight + ACTIVE |
| Stabilization | `stabilize_confidence` pulls toward evidence mass |
| Stale detection | Idle since `last_reinforced` ≥ threshold → `STALE` uncertainty |
| Obsolete handling | Very low weight after long neglect → `OBSOLETE` influence (IDs retained) |

## Non-goals

- No provenance deletion
- No Experience erasure
- No moving decay into Forgetting organ
- No calibrated psychometrics (B22)

## Certification

- Behavioral: `tests/behavioral/test_m5_evidence_weighting.py`
- Learning: `tests/cognitive/test_m5_evidence_decay_learning_cert.py` (L13–L14)
