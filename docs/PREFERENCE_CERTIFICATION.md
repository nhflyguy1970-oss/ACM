# Preference Behavioral Certification — v0.21.0

**Status:** CERTIFIED (standalone ACM)  
**Date:** 2026-07-17  
**Version:** 0.21.0  
**Scope:** Standalone ACM reference implementation only — not promoted into Aria.

## Live blocker (evidence)

Live Aria answered:

```
What is my favorite color?
→ Your preference is Tool `memory_search` worked for:
  Show the evidence for my favorite color.
```

Aria was used only as evidence. All corrections are in this repository.

## Root causes

1. **Artifact classifier gap** — D047 matched bare-word
   ``Tool memory_search worked for:`` but missed live backtick-quoted
   ``Tool `memory_search` worked for:``.
2. **Cleanup skip** — experiences with empty metadata / without
   ``semantic_extraction`` were treated as internal cognition even when the
   summary was a tool wrapper.
3. **Provenance-only trust** — D046 evaluated declared provenance; hosts can
   mislabel tool output as trusted user speech.
4. **Interrogative / fallback preference minting** — questions and unmatched
   ``favorite`` mentions minted preference attributes via Semantic Extraction
   and concept cues (``conflicting?``, full tool strings).
5. **Renderer** — reconstruction answered from non-user artifact attribute
   values; generic ``preference`` keys competed with ``favorite_*``.

## Corrections

| Surface | Correction |
|---------|------------|
| `acm.provenance.legacy_cleanup` | Backtick tool wrappers + host autosave; content-artifact condemnation without metadata; orphaned artifact-valued attribute removal |
| `acm.authority.protection` | Content-level trust rejection of artifact payloads |
| `acm.semantic.facts` | Interrogatives never mint preference facts |
| `acm.concepts.extract` | Interrogatives never mint preference cues; no full-text preference dump |
| `acm.remembering.organ` | Refuse artifact attribute values; prefer ``favorite_*`` over generic ``preference`` |

Architecture preserved. No organ redesign. No Memory Authority redesign.
No Semantic Extraction redesign beyond the interrogative/fallback guards.
No Reconstruction redesign beyond proven failure modes.

## Certified behavior

| Step | Expected | Result |
|------|----------|--------|
| Fresh store → favorite color? | Unknown | Pass |
| Teach blue | Blue | Pass |
| Teach blue again | No duplicate active attribute | Pass |
| Teach red | Red; blue retired | Pass |
| Restart | Red | Pass |
| Inject prior contamination strings | Ignored (`memory_trust`) | Pass |
| Show evidence | Evidence returned; memory unchanged | Pass |
| Repeat contamination | Still red | Pass |
| Live-format contaminated graph + cleanup | Blue restored | Pass |
| Identity regression | Jeff preserved | Pass |
| D046 provenance gate | Untrusted rejected | Pass |
| D047 fixture cleanup | 5 removals; blue restored; idempotent | Pass |

Suite: `tests/cognitive/test_preference_certification.py`

## Why previous validation passed

- D047 fixtures used bare-word tool wrappers that the classifier already matched.
- D046 tests declared tool provenance correctly; they did not mislabel tool
  *content* as trusted user speech.
- Preference certification against live Aria formats had not yet been run.

## Promotion

**Do not promote into Aria until explicit approval.**
