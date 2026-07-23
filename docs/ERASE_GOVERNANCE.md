# Erase / Forget / Prune Assent UX — B36

**Status:** Implemented (ACM v0.42.0)  
**Depends on:** B07–B09 · B14 · ForgettingOrgan

## Purpose

Explicit user governance for high-impact pruning, soft forgetting, and legal
erase requests — without silent Experience deletion.

## Operations

| Op | Effect |
|----|--------|
| `soft_forget` | Deactivate living attributes; cool related concepts |
| `prune` | Mark prune-eligible (proposal stage only) |
| `legal_erase` | Soft-forget + purge related envelopes; audit lineage |

Experiences are **never** physically deleted. Identity names cannot be
soft-forgotten (use B20 identity correction).

## APIs

`preview_erase_request` · `propose_erase_request` · `assent_erase_request` ·
`reject_erase_request` · `cancel_erase_request` · `apply_erase_request` ·
`pending_erase_requests`

## Validation

Cognitive / behavioral / learning (L32) / long-duration suites.
