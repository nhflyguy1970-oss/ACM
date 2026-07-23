# Preference Correction UX — B12

**Status:** Implemented (ACM v0.38.0)  
**Depends on:** B11

## Purpose

Distinguish a preference **correction** (“Actually…”) from a plain new
observation, preserving correction lineage on the authorizing Experience.

## APIs

- `preview_preference_correction(text)`
- `apply_preference_correction(text, assent=True)`

Commits reuse B11 encode supersede; correction lineage is recorded on a
side-channel (`engine._preference_corrections`) because Experiences are frozen.

## Validation

Cognitive / behavioral / learning gate L28.
