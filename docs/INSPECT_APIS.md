# Non-Mutating Inspection APIs (B08)

**Status:** Normative  
**Depends on:** [READ_ONLY_DIAGNOSTIC_MODE.md](READ_ONLY_DIAGNOSTIC_MODE.md) (B07)

## Purpose

Stable façades for diagnostic hosts to inspect reconstruction, evidence,
confidence, identity, and conflict **without** living-memory mutation.

These APIs are read-models over Memory Authority. They do not invent a second
cognitive path and do not grant direct store authority.

## API

```python
engine.inspect_reconstruction(cue)
engine.inspect_evidence(cue)
engine.inspect_confidence(cue)
engine.inspect_identity(who="user"|"assistant")
engine.inspect_conflict(cue)
```

Each returns a versioned schema (`acm.inspect.*.v1`) plus `execution_mode` and a
`fingerprint` snapshot for zero-write assertions.

## Guarantees

- Same classify → route → dispatch organs as ordinary cognition
- Always under `ExecutionMode.READ_ONLY`
- Store / buffer / context fingerprints unchanged across calls
- Normal `cognitive_respond` / `remember` still reconsolidate as designed

## Non-goals

- B09 diagnostic safety / redaction policy
- B02 evidence-introspection *intent* for conversational speech
- Host UI / Mission Control presentation

## Validation

`tests/cognitive/test_inspect_apis.py`
