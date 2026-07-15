# Observability

Observable **cognitive state**, not reasoning dumps.

## Principles

- No prompts
- No chain-of-thought
- No hidden “why I chose token X”
- Yes: activations, associations, confidence deltas, lifecycle, working transitions, reconsolidation, sleep, identity touches

## Validation Harness

`CognitiveEngine.validation` → `ValidationHarness`

```python
report = engine.validation.snapshot()
assert report["schema"] == "acm.validation/0.7"
```

Recorded streams (trimmed FIFO):

| Stream | Meaning |
|--------|---------|
| `activations` | Cue → activated concepts + cue classes |
| `confidence_deltas` | Before/after confidence with reason code |
| `association_changes` | Legacy edge add/strengthen/weaken residual |
| `lifecycle` | Encode / goal / other verb events |
| `working_transitions` | Enter / displace |
| `reconsolidations` | Light / supersede / contest |
| `sleep_events` | Prune counts + proposals |
| `identity_touches` | Identity-concept activity |
| `identity` (aggregate) | growth · stability · change · confidence · influence · lineage · evolution |
| `experience_events` / `experience` | M2 metrics |
| `concept_events` / `concept` | M3 metrics |
| `association_events` / `association` | M4 metrics |
| `remembering_events` | Activation fields + reconstructions |
| `remembering` (aggregate) | reconstructions · activations · ambiguities · propagations · decays · experience_participants · goal/identity/context/working influence · evolution |
| `reflection_events` | Evaluation outcomes + Reflective Experience ids |
| `reflection` (aggregate) | reflections · contradictions · patterns · questions · hypotheses · insufficient_evidence · activation_reused · reflective_experiences · evolution |

## Trace log

`CognitiveEngine.trace` holds `CognitiveTraceEvent` records suitable for export/dashboard adapters **outside** ACM.

Public fields include: verb, attention_class, context_tags, goal_ids, activated_concept_ids, association_edge_types, explanation_class, reconsolidation, latency_ms, metadata.
