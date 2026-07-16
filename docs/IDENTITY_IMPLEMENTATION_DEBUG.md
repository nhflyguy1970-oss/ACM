# Identity Implementation Debug

**Status:** Accepted (D042) · **Version:** v0.18.1

## Problem

After Semantic Extraction correctly classified `My name is Jeff.` as user identity,
`Who am I?` still answered with low-confidence refusal in behavioral validation.

## Root cause (evidence-based)

Not a missing organ. Not an architecture gap.

**Loss point:** post-extraction Concept ingest colliding with the Identity user schema,
plus Identity retrieval confidence keyed off schema nucleus confidence instead of the
stored name attribute.

| Question | Answer |
|----------|--------|
| Did extraction produce the fact? | Yes — User · Name · Jeff |
| Was it stored on user schema? | Yes — attribute name=Jeff @ 0.92 |
| Was it polluted? | Yes — `mentioned=user` from cue label collision |
| Was confidence reduced? | Yes — retrieval used schema.confidence (~0.4–0.56) |
| Was architecture wrong? | No — implementation defect only |

## Confidence explanation

- Attribute adopt sets name confidence ≈ `min(0.92, 0.55 + weight/2)`.
- Schema nucleus starts at ~0.4 and only slowly strengthens.
- Gate `MIN_KNOWN_CONFIDENCE = 0.42` → empty/weak schema path refuses; attribute path must be used.
- After fix: retrieval confidence = **0.92** (name attribute) → status `known`.

## Validation

`tests/cognitive/test_identity_pipeline_debug.py` proves store → retrieve → speak.

## Non-goals

No new organs. No dispatch/authority redesign. No Aria promotion in this release.
