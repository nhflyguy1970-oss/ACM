# Preference Conflict Analysis — Root Cause

**Investigation:** Preference subsystem — false `competing_recollections`
**Date:** 2026-07-17
**Status:** Root cause conclusively identified. Investigation only — no fix
implemented. See `PREFERENCE_PIPELINE_TRACE.md` for the full trace and
`PREFERENCE_INTROSPECTION.md` for the diagnostic-question analysis.

---

## Observed behavior (reproduced)

```text
Fresh memory:  What is my favorite color?   → unknown            PASS
Teach:         My favorite color is blue.
Ask:           What is my favorite color?   → conflicting (competing_recollections)
Why…conflicting? / Show the evidence…       → conflicting (competing_recollections)
```

Reproduced deterministically in the standalone ACM whenever at least one
additional sentence containing the word "favorite" (typically the user's own
question, logged as a conversation turn) is encoded alongside the teach.

## Root cause

**Conflict detection in `RememberingOrgan._reconstruct`
(`acm/remembering/organ.py`) admits lexical token-nucleus concepts as
competing recollections.** The reported "conflict" is the word *favorite*
itself — an ENTITY concept with attribute `mentioned='favorite'` created as
emergence fuel during encoding — not a contradictory preference.

### The actual competing facts (measured)

| | Concept | Role | Attribute | Nature |
|---|---|---|---|---|
| Winner | `favorite color` | `preference` | `favorite_color='blue'` | The real, single preference fact |
| "Rival" | `favorite` | `entity` | `mentioned='favorite'` | Word-frequency record from turn encoding |

The store contains **exactly one active preference fact**. No duplicate, no
contradiction. The rival's answer preview rendered by
`_format_from_concept` is the literal string `"favorite."`.

### Failure mechanism (four interacting weaknesses)

1. **Token nuclei are renderable.** `extract_cues`
   (`acm/concepts/extract.py`) creates ENTITY concepts for content words with
   `mentioned=<word>` attributes, and `_format_from_concept` will render a
   `mentioned` attribute as an answer whenever the cue shares that token —
   so a bare word can masquerade as a recollection.
2. **Rival admission has no semantic/role filter.** The `_reconstruct` rival
   loop admits any concept within `COMPETE_RATIO = 0.88` of the top energy
   whose labels/attributes overlap a cue token (`_cue_relevant`). For a
   preference cue, a `preference`-role winner can be "contested" by an
   `entity`-role token nucleus. `_cue_relevant` is trivially true for token
   nuclei because the rival *is* a cue word.
3. **Re-mention inflation.** Every encoded sentence containing "favorite"
   re-ingests the same token concept, raising its confidence/strength and
   hence its activation energy. Measured rival/top ratio: 0.755 after the
   teach alone (healthy, below 0.88) → 0.902 after one question turn →
   conflict. The defect therefore appears only in conversational use, which
   is why organ-level tests (`tests/behavioral/test_preference_memory.py`)
   pass while behavioral sessions fail.
4. **Interrogative fallback stores question text as a preference.** In
   `extract_cues`, any sentence matching `/prefer|favorite/` that fails the
   `favorite X is Y` regex falls into a fallback branch that stores the raw
   text — so the encoded question turn creates
   `preference='What is my favorite color?'` on a second preference-role
   concept, adding more energy to the neighborhood.

### Gate behavior is correct given its input

`gate_status` (`acm/authority/gates.py`) maps `ambiguous=True` →
`CONFLICTING` → `competing_recollections`. The gate faithfully reports what
reconstruction told it; the ambiguity flag itself is wrong.

## Hypotheses ruled out (with evidence)

| Hypothesis | Verdict | Evidence |
|---|---|---|
| Duplicate extraction | **No** | `extract_semantics` yields exactly one fact for the teach; zero for the question. |
| Duplicate storage | **No** | Repeated identical teach dedupes to one active attribute; retrieval stays `known`. |
| Existing preference facts | **No** | Reproduced from a fresh store. |
| Contradictory facts | **No** | Only one active `favorite_color` attribute exists at conflict time. `blue→red` correctly deactivates the old value (last-write-wins SET semantics) and returns `known`. |
| Confidence scoring | **Contributing only** | Confidence values are sane; the clamp to ≈0.56 is a *consequence* of the false ambiguity. |
| Reconstruction logic | **ROOT CAUSE** | Rival admission in `_reconstruct` (see mechanism above). |
| Conflict detection thresholds | **Contributing** | `COMPETE_RATIO=0.88` is crossed only because token nuclei inflate with re-mention; the threshold is not itself the defect. |
| Rendering | **Contributing (introspection)** | The CONFLICTING template never names the competing facts. |
| Routing | **Contributing (introspection)** | Preference cue swallows evidence requests; no teach/query discrimination. |
| Dispatcher behavior | **No** | Dispatch path is correct: `intent:preference → owner:remembering → terminate:remembering`. |

## Defect classification

- **Primary:** Reconstruction / conflict detection
  (`acm/remembering/organ.py :: _reconstruct` + `_format_from_concept` +
  `_cue_relevant`).
- **Contributing:** Concept cue extraction
  (`acm/concepts/extract.py :: extract_cues` — renderable token nuclei;
  interrogative fallback branch).
- **Contributing:** Intent classification
  (`acm/authority/classification.py` — no declarative-teach or
  evidence-inspection discrimination; see `PREFERENCE_INTROSPECTION.md`).
- **Not defective:** semantic extraction, preference fact storage/update,
  gates, dispatch, speak templates (given correct status).

## Secondary finding — diagnostic queries mutate memory

Retrieval is not read-only in the presence of the false conflict:

- Each query reconsolidates the top concept (+confidence, association
  reinforcement).
- Each reflection dispatch on the ambiguous reconstruction births a
  CONTRADICTION reflective experience, which learning consumption converts
  into concept/association **weakening** ("Weakened association after
  contradiction", `acm/learning/organ.py`).

Measured over four consecutive diagnostic queries the true preference
concept's confidence drifted 0.825 → 1.000 while contradiction records
accumulated. A user probing a false conflict therefore *changes* the memory
state they are inspecting.

## Recommended implementation correction (for review — NOT implemented)

Smallest correction consistent with the existing architecture:

1. In `_reconstruct`, exclude rivals whose only cue relevance is a
   token-nucleus `mentioned` attribute (or whose role is ENTITY when the
   winner is a PREFERENCE-role concept answering a preference cue) — a
   competing *recollection* must itself be capable of answering the cue with
   a non-lexical attribute.
2. In `_format_from_concept`, never render a bare `mentioned` attribute as an
   answer preview for competition purposes.
3. In `extract_cues`, do not store interrogative sentences as preference
   attributes (fallback branch should require a declarative form).

Items 1–2 remove the false conflict; item 3 removes the spurious stored
question text. Classification improvements (teach vs. query, evidence intent)
are introspection-quality improvements documented separately and need a
decision on scope.

## Reproduction and executable evidence

- `tests/cognitive/test_preference_pipeline_debug.py` — 11 diagnostic tests:
  healthy stages (unknown / single / repeated / update / reconstruction) pass
  as designed; `test_defect_*` tests reproduce and pin the defective behavior
  for the record. These assertions must be updated when the approved
  correction lands.
