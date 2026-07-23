# B46 — Legacy Identity Extraction Closure

**Status:** FORMALLY CLOSED (COMPLETE without retirement) — ACM v0.44.0  
**Date:** 2026-07-23

## Decision

Do **not** remove `IdentityOrgan._extract_identity_attribute` or the legacy
classification fallback in this platform release.

## Why not retire

Semantic Extraction does **not** yet cover the full Daily Use identity corpus
with zero `raw_fallback`. Sample gaps observed 2026-07-23:

| Utterance | Semantic result |
|-----------|-----------------|
| `My legal name is Jeffrey Richardson.` | `raw_fallback=True`, no identity fact |
| `I am known as Aria.` | `raw_fallback=True`, no identity fact |

Retiring the legacy path before corpus parity would regress encode fidelity for
odd but real identity phrasings (B46 acceptance criterion unmet).

## What remains

- Structured facts remain the primary path when `extract_semantics` succeeds.
- Legacy regex is a **fallback only** when structured facts are absent.
- Relationship possessives (e.g. dog’s name) are handled by semantic extraction
  and B47 recall — not by legacy user-name write.

## Re-open condition

Re-open B46 as an implementation task only after a certified extract-vs-legacy
corpus shows semantic coverage of all Daily Use identity phrasings with
`raw_fallback=False` and no perspective/subject drift.

## Related

- `docs/IDENTITY_EXTRACTION.md`
- `acm/identity/organ.py` (`_extract_identity_attribute`, classify fallback)
- Backlog B46
