# Preference Pipeline Trace

**Investigation:** Preference subsystem — false `competing_recollections`
**Date:** 2026-07-17
**Status:** Diagnostic complete — root cause identified (see
`PREFERENCE_CONFLICT_ANALYSIS.md`). No behavior was changed.

This document traces the complete pipeline for the teach statement
`"My favorite color is blue."` and the retrieval question
`"What is my favorite color?"`, identifying every decision point.

---

## 1. Natural language → Intent classification

`acm/authority/classification.py :: classify_memory_request`

| Utterance | Intent | Signal | Owner |
|---|---|---|---|
| `What is my favorite color?` | `preference` (0.93) | `preference_cue` | remembering |
| `My favorite color is blue.` | `preference` (0.93) | `preference_cue` | remembering |
| `Why do you think my favorite color is conflicting?` | `reflection` (0.93) | `reflection_cue` | reflection |
| `Show the evidence for my favorite color.` | `preference` (0.93) | `preference_cue` | remembering |

**Decision points:**

- The `preference_cue` pattern (`\b(prefer…|favorite|favourite|…)\b`) matches
  *any* sentence containing the word "favorite" — declarative teach,
  interrogative question, and evidence request alike.
- There is **no declarative/teach discrimination**: the teach statement
  classifies as a retrieval-style memory request and is routed to remembering.
- There is **no evidence/introspection intent** in the taxonomy; the evidence
  request is swallowed by `preference_cue` (see
  `PREFERENCE_INTROSPECTION.md`).

## 2. Semantic extraction (teach path)

`acm/semantic :: extract_semantics("My favorite color is blue.", kind="preference")`

Produces exactly **one** structured fact — correct:

```text
CognitiveFact(kind=PREFERENCE, subject=USER, property='favorite_color',
              value='blue', confidence=0.85, update_op=SET)
```

`extract_semantics("What is my favorite color?")` correctly produces **zero**
facts (questions are not facts).

## 3. Structured preference facts → Preference storage

`acm/api/engine.py :: encode` →
`acm/concepts/organ.py :: ingest_from_encode` → `acm/concepts/extract.py :: extract_cues`

For the teach sentence, `extract_cues` emits:

| Cue | Role | Attribute |
|---|---|---|
| `favorite color` | PREFERENCE | `favorite_color='blue'` ✅ the real fact |
| `favorite` | ENTITY | `mentioned='favorite'` ← token nucleus |
| `color` | ENTITY | `mentioned='color'` ← token nucleus |
| `blue` | ENTITY | `mentioned='blue'` ← token nucleus |

**Decision points:**

- Token nuclei ("emergence fuel", extract.py lines 129–143) are stored as
  first-class concepts with renderable `mentioned` attributes.
- If a *question* containing "favorite" is encoded as a conversation turn, the
  preference branch of `extract_cues` fails the `favorite X is Y` regex and
  falls into the fallback branch, storing the **raw interrogative text** as
  `preference='What is my favorite color?'` on a `preference` concept —
  a spurious preference fact.
- Every re-mention of "favorite"/"color" in later turns **re-ingests and
  strengthens** the same token-nucleus concepts (confidence, strength,
  association weights all grow).

Storage of the actual preference is correct: repeated identical teaches
deduplicate onto one attribute; `blue → red` updates deactivate the old value
(`active=False`) and activate the new one. Verified by
`tests/cognitive/test_preference_pipeline_debug.py`.

## 4. Retrieval: activation → reconstruction

`acm/remembering/organ.py :: what_do_i_remember` → `_reconstruct`

Activation field for `"What is my favorite color?"` after a healthy teach plus
**one** encoded question turn (measured):

| Concept | Role | Energy | Ratio to top |
|---|---|---|---|
| `favorite color` | preference | 1.072 | 1.000 |
| `favorite` | entity | 0.967 | **0.902** |
| `color` | entity | 0.883 | 0.823 |
| `preference` (question text) | preference | 0.828 | 0.772 |

**Decision points (the defect lives here):**

1. Top concept `favorite color` renders correctly:
   `_format_from_concept` → `"Your favorite color is blue."`,
   `ExplanationClass.PREFERENCE`.
2. Rival admission loop (`_reconstruct`, rivals within
   `COMPETE_RATIO = 0.88` of top energy):
   - `favorite` (0.902 ≥ 0.88) — admitted.
   - `_cue_relevant('favorite', tokens)` — trivially **True**: the rival
     concept *is* one of the cue words.
   - `_format_from_concept` renders its `mentioned='favorite'` attribute as
     the answer preview `"favorite."` — different from the top answer, so it
     is recorded as a `CompetingRecollection`.
3. `ambiguous = True`, confidence clamped to ≈0.56.

## 5. Conflict detection → Gate → Final CognitiveMemoryResult

`acm/authority/gates.py :: gate_status`

```text
ambiguous=True → MemoryStatus.CONFLICTING
→ uncertainty_label → "competing_recollections"
```

`acm/authority/speak.py` renders:

> "I have conflicting memories and cannot settle on a single answer yet."

Final result (measured):

```text
status=conflicting  confidence≈0.56–0.59  uncertainty=competing_recollections
memory='Your favorite color is blue.'   ← the correct answer is present!
reasoning_path=… gate:conflicting terminated_at:remembering
```

Note the reconstruction **did** find the single correct answer; the gate
demoted it because of the false rival.

## 6. Evidence retrieval / Renderer

- `supporting_experiences` correctly cite the teach experience
  (`favorite color is blue`).
- Provenance chain is intact (encode → experience → concept contributors).
- The renderer (`speak.py`) has a fixed template per status; for CONFLICTING
  it never surfaces *which* recollections compete.

## 7. State-dependence of the defect (measured)

- Teach only (1 encode): rival ratio 0.755 → **known**. Healthy.
- Teach + 1 question turn: ratio 0.902 → **conflicting** for the short cue.
- Teach + 2 question turns: **conflicting** for both short and long cues
  ("Show the evidence…").
- Each retrieval *mutates* state: reconsolidation (+0.01 concept confidence,
  association reinforcement) and, on the reflection path, learning
  consumption **weakens** concepts/associations after CONTRADICTION outcomes
  ("Weakened association after contradiction"). Measured drift of the true
  preference concept across four queries: confidence 0.825 → 1.000 while the
  conflict persisted.

## Reproduction (minimal)

```python
from acm import CognitiveEngine, TRUSTED_USER_STATEMENT
eng = CognitiveEngine(agent_id="repro")
eng.encode(
    "My favorite color is blue.",
    kind="preference",
    provenance=TRUSTED_USER_STATEMENT,
)
eng.encode(
    "What is my favorite color?",
    provenance=TRUSTED_USER_STATEMENT,
)
eng.cognitive_respond("What is my favorite color?")
# → status='conflicting', uncertainty='competing_recollections'
```

Executable form: `tests/cognitive/test_preference_pipeline_debug.py`
(`test_defect_false_conflict_from_token_nucleus_concept`).
