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
assert report["schema"] == "acm.validation/0.2"
```

Recorded streams (trimmed FIFO):

| Stream | Meaning |
|--------|---------|
| `activations` | Cue → activated concepts + cue classes |
| `confidence_deltas` | Before/after confidence with reason code |
| `association_changes` | Edge add/strengthen/weaken |
| `lifecycle` | Encode / goal / other verb events |
| `working_transitions` | Enter / displace |
| `reconsolidations` | Light / supersede / contest |
| `sleep_events` | Prune counts + proposals |
| `identity_touches` | Identity-concept activity (adopt / strengthen / propose / assent / influence / …) |
| `identity` (aggregate) | growth · stability · change · confidence · influence · lineage · evolution |

## Trace log

`CognitiveEngine.trace` holds `CognitiveTraceEvent` records suitable for export/dashboard adapters **outside** ACM.

Public fields include: verb, attention_class, context_tags, goal_ids, activated_concept_ids, association_edge_types, explanation_class, reconsolidation, latency_ms, metadata.
