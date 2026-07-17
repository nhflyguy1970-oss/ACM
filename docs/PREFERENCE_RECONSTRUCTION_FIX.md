# Preference Reconstruction Fix (D045)

**Version:** v0.18.4  
**Date:** 2026-07-17  
**Status:** Implemented in standalone ACM. Promotion into Aria requires
separate approval.

## Problem

After teaching a single preference (`My favorite color is blue.`), retrieval
returned `competing_recollections` whenever the user's own question had also
been encoded as a conversation turn. The store held exactly one active
preference fact. Behavioral sessions failed; organ-level preference tests
passed.

## Root cause

Documented in `PREFERENCE_CONFLICT_ANALYSIS.md` (D045 investigation):

`RememberingOrgan._reconstruct` admitted lexical token-nucleus concepts
(ENTITY concepts whose only content is `mentioned=<word>`) as competing
recollections. Re-mention of the cue word across conversation turns pushed
those nuclei inside `COMPETE_RATIO` of the true preference concept → false
`ambiguous=True` → gate `CONFLICTING` → `competing_recollections`.

Additionally, when re-mention inflation made a lexical concept the
top-ranked node, `_format_from_concept` fell through to a bare-label answer
(`"favorite."`), so the lexical concept could become the primary answer.

## Implementation

Smallest correction inside `acm/remembering/organ.py`. No new organs. No
architecture change. Competition thresholds, energy model, extraction,
storage, dispatch, routing, learning, and reflection are untouched.

### 1. Answerability admissibility

A concept may be the **primary** recollection or a **competing** recollection
only if `_answerable(concept, tokens)` is true:

- At least one active **semantic** attribute grounds in the cue.
- Lexical support keys (`mentioned`, `cue`, `token`, `surface`, `lexeme`,
  `index`, `stem`, …) never count.
- Interrogative values that merely restate the cue
  (`preference='What is my favorite color?'`) never count as independently
  answerable content.

Lexical support concepts remain in the activation field and continue to
support cueing / emergence. They are simply excluded from primary selection
and ambiguity scoring.

### 2. Rendering exclusion

`_format_from_concept` never selects lexical support attributes as cognitive
answers. Concepts whose only active content is lexical metadata return
`UNKNOWN` rather than falling through to a bare-label `"favorite."` answer.

### Explicitly deferred (unchanged)

- Teach vs query classification
- Evidence intent
- Preference introspection / reflection explanation quality
- Diagnostic query mutation
- Preference editing UX
- Stopping `extract_cues` from storing interrogative text as preference
  attributes (reconstruction now ignores those values for answerability;
  storage cleanup remains a separate decision)

## Behavior before

```text
Teach: My favorite color is blue.
Encode: What is my favorite color?   # conversation turn
Ask:    What is my favorite color?
→ status=conflicting  uncertainty=competing_recollections
  rival = ENTITY 'favorite' (mentioned='favorite')
```

## Behavior after

```text
Teach: My favorite color is blue.
Encode: What is my favorite color?   # conversation turn
Ask:    What is my favorite color?
→ status=known  memory='Your favorite color is blue.'
  competing=[]  ambiguous=False
  token nucleus 'favorite' still activates in the field (retrieval support)
```

True semantic conflicts are preserved:

```text
Teach: My favorite color is blue.
Teach: My favourite colour is red.   # distinct semantic concept
Ask:   What is my favorite color?
→ status=conflicting  uncertainty=competing_recollections
  rival answer_preview = 'Your favorite colour is red.'
```

## Architectural invariants preserved

- Cognitive Activation Architecture unchanged
- `COMPETE_RATIO` / energy model unchanged
- Semantic Extraction unchanged
- Preference storage / update (SET + deactivate) unchanged
- Intent taxonomy, routing, dispatch, gates, speak templates unchanged
- Token nuclei / emergence fuel still formed and still support retrieval
- No new cognitive organs

## Validation

- `tests/cognitive/test_preference_reconstruction_fix.py` — full behavioral
  matrix (unknown, teach/retrieve, repeated, update, lexical never ambiguous,
  true conflict, rendering, answerability)
- `tests/cognitive/test_preference_pipeline_debug.py` — D045 false-conflict
  case now asserts known; deferred defects remain pinned
- Full suite, ruff, host-independence check

## Related

- Investigation: `PREFERENCE_PIPELINE_TRACE.md`,
  `PREFERENCE_CONFLICT_ANALYSIS.md`, `PREFERENCE_INTROSPECTION.md`
- Decision: **D045** (diagnosis + correction)
