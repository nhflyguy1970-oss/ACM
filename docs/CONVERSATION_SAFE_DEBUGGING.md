# Conversation-Safe Debugging — B10

**Status:** Implemented (ACM v0.36.0)  
**Depends on:** B07 · B08 · B09 · B27

## Purpose

Trace live conversational cognition (classify → route → reconstruct) without
contaminating the autobiographical store or influencing subsequent activation.

## Policy

| Setting | Default |
|---------|---------|
| `enabled` | **False** (opt-in; production off) |
| `max_captures` | 64 side-channel ring (not Experiences) |
| `include_organ_view` | optional B27 organ name |

```python
CognitiveEngine(
    conversation_debug_policy=ConversationDebugPolicy(enabled=True)
)
engine.debug_capture(cue)
engine.debug_capture_replay(cue)  # equivalence check
engine.debug_captures_recent()
```

`force=True` allows one-shot capture in tests without enabling policy.

## Guarantees

- Always uses B07 `READ_ONLY` for reconstruction
- B09 safety applied to capture envelope
- No new Experiences / Concepts / Associations
- Fingerprint unchanged across capture
- Repeated debugging leaves ordinary answers unchanged
- Capture buffer is a side channel — never Memory Authority

## Non-goals

- Host Trace UI
- Encoding debug questions as Experiences
- Shadow host adapters (ops)

## Validation

- Cognitive / behavioral / learning (L26) / long-duration tests
