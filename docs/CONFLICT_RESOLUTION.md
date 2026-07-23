# User-Assisted Conflict Resolution — B13

**Status:** Implemented (ACM v0.39.0)  
**Depends on:** B04 · B08 · B11 · B12

## Purpose

Interactive confirm / reject / abstain when competing recollections answer the
same cue — without last-write-wins evidence loss.

## APIs

- `open_conflict_resolution(cue, key="")`
- `confirm_conflict_resolution(session_id, chosen)`
- `reject_conflict_resolution(session_id)`
- `abstain_conflict_resolution(session_id)`

Confirm applies via B11 preference edit; retired values remain in attribute
versions.

## Validation

Cognitive / behavioral / learning gate L29.
