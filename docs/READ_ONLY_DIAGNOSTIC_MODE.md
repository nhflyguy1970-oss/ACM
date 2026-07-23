# Read-Only Diagnostic Mode (B07)

**Status:** Normative  
**API:** `CognitiveEngine.inspect` · `acm.authority.mode.read_only`

## Purpose

Diagnostic inspection of cognition must not alter the memory being inspected.

Ordinary recall remains biologically inspired update-on-retrieval (P2).
Diagnostics use an explicit **read-only execution mode**.

## Modes

| Mode | Behavior |
|------|----------|
| `NORMAL` (default) | Reconsolidation, reflective birth, learning, buffer writes as designed |
| `READ_ONLY` | Reconstruct / classify / route / speak without living-memory mutation |

## API

```python
# Preferred diagnostic entry
result = engine.inspect("What is my favorite color?")

# Or scoped context
from acm.authority.mode import read_only
with read_only():
    result = engine.cognitive_respond("Why is this conflicting?")

# Zero-write assertions
before = engine.store_fingerprint()
engine.inspect(cue)
assert engine.store_fingerprint() == before
```

`diagnostics.execution_mode` reports `"read_only"` or `"normal"`.

## Suppressed side effects

Under `READ_ONLY`:

- Light reconsolidation (confidence / strength / association reinforce)
- Strong-cue reactivation and priority investment
- Working-buffer push
- Reflective Experience birth
- Learning adaptations
- Prediction / reconciliation / simulation store inserts
- Declarative teach encode in the response pipeline
- Accessibility map materialization via `ForgettingOrgan.ensure`
- Context-frame updates on remember / reflect

## Preserved

- Classification, ownership, dispatch
- Activation and reconstruction
- Faithful speech / Memory Authority gates
- Normal mode behavior when not inspecting

## Non-goals (later backlog)

- B08 — stable non-mutating inspection façades
- B09 — diagnostic safety / redaction policy
- B10 — conversation-safe debugging capture
- B29 — privacy redaction

## Validation

`tests/cognitive/test_read_only_diagnostic_mode.py`
