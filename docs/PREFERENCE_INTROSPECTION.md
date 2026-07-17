# Preference Introspection Analysis

**Investigation:** Why diagnostic questions cannot explain the preference conflict
**Date:** 2026-07-17
**Status:** Historical D045 investigation. The false lexical conflict was fixed
in v0.18.4; teach/query classification, evidence intent, reflection explanation,
and diagnostic mutation remain deferred.

Companion documents: `PREFERENCE_PIPELINE_TRACE.md`,
`PREFERENCE_CONFLICT_ANALYSIS.md`.

---

## Question investigated

After the false `competing_recollections` appears, every diagnostic question
terminates with the identical status:

```text
Why do you think my favorite color is conflicting?  → competing_recollections
Show the evidence for my favorite color.            → competing_recollections
```

Are these incorrectly routed to the same terminal response, and if so, where
is introspection bypassed?

## Finding 1 — Evidence requests are swallowed by the preference cue

`"Show the evidence for my favorite color."`

- Classification (`acm/authority/classification.py`, Band B): the
  `preference_cue` pattern matches on the word "favorite" and returns
  `intent=preference` before any other consideration.
- **There is no evidence/introspection intent in the taxonomy**
  (`acm/authority/taxonomy.py`). Nothing in Band B recognizes "show the
  evidence", "what supports", or similar cues.
- Routing then sends it to the same `remembering` terminal as the base
  question, which re-runs the same reconstruction and hits the same false
  ambiguity → identical `competing_recollections` terminal.

**Introspection is bypassed at intent classification.** The pipeline never
reaches any component that could enumerate supporting experiences or
provenance — even though that evidence exists and is attached to every
result (`supporting_experiences`, `provenance` are populated correctly).

## Finding 2 — Conflict explanation reaches reflection but cannot name the conflict

`"Why do you think my favorite color is conflicting?"`

- Classification: `reflection_cue` ("why do you think") → `intent=reflection`
  → reflection organ. Routing is *reasonable* here.
- `ReflectionOrgan.what_do_i_think` re-runs the same remembering
  reconstruction, sees `ambiguous=True`, and emits a CONTRADICTION outcome.
  Internally it *does* record the competitor
  (`"Competing recollection: favorite ≈ favorite."`) in
  `evaluation.contradictions`.
- But the dispatched memory text is the generic template summary —
  *"I remember something about this, but evidence conflicts
  (assessment=0.50). Multiple interpretations remain plausible."* — plus
  learning-adaptation strings. The specific competing facts in
  `contradictions` are **never rendered** into the terminal answer.
- The result then gates on the same ambiguous reconstruction → status
  `conflicting` / `competing_recollections` again.

So the explanation query is not misrouted, but its answer is
**non-explanatory**: the renderer drops the very evidence
(`contradictions[]`) that would answer the user's question.

## Finding 3 — Diagnostic questions mutate the memory under inspection

Asking "why is this conflicting?" is not read-only:

1. Reflection births a CONTRADICTION reflective experience.
2. Learning consumption (`acm/learning/organ.py`) converts contradiction
   outcomes into concept/association **weakening**
   ("Weakened association after contradiction.",
   "Reduced confidence after reflective contradiction.") — these strings
   appeared verbatim in the observed behavioral session output.
3. Simultaneously, each retrieval reconsolidates the top concept
   (+0.01 confidence, association reinforcement).

Measured across four consecutive diagnostic queries, the true preference
concept drifted from confidence 0.825 to 1.000 with contradiction records
accumulating. Repeatedly interrogating a false conflict therefore rewrites
the evidence trail.

## Finding 4 — The teach statement itself is answered as a query

`"My favorite color is blue."` classifies as `intent=preference`,
`is_memory_request=True`, primary organ `remembering` — i.e., a retrieval.
There is no declarative/teach discrimination in classification. In a
conversational session where each turn is dispatched, the *reply to the
teach* is a retrieval result over the just-contaminated store — which is
exactly the reported arrow:

```text
Teach: My favorite color is blue.
→ "I have conflicting memories and cannot settle on a single answer yet."
```

## Where introspection is bypassed — summary

| Diagnostic question | Bypass point | Component |
|---|---|---|
| "Show the evidence…" | Intent classification: no evidence intent; `preference_cue` wins | `acm/authority/classification.py` / `taxonomy.py` |
| "Why … conflicting?" | Rendering: reflection's `contradictions[]` never reach the terminal answer | `acm/authority/handlers.py :: _reflection` + `speak.py` |
| (both) | Status gating: re-gates on the same false-ambiguous reconstruction | consequence of the root cause in `remembering/organ.py` |

## Executable evidence

`tests/cognitive/test_preference_pipeline_debug.py`:

- `test_deferred_evidence_inspection_bypassed_to_preference`
- `test_deferred_teach_statement_classified_as_retrieval`

D045 changed reconstruction admissibility only. Any correction to
classification precedence, an evidence-inspection intent, contradiction
rendering, or diagnostic mutation still requires review and approval. These
items are tracked in `ENGINEERING_BACKLOG.md`.
