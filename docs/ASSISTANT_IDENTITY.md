# Assistant Identity

**Status:** Normative (v0.18.2)  
**Decision:** D043

## Claim

Assistant Identity is **operational** (intrinsic / configuration), not autobiographical
memory learned from the user’s conversation.

| Field | Source |
|-------|--------|
| Name | `assistant_identity.name` or `agent_id` |
| Role | configuration |
| Description | configuration |
| Capabilities | configuration |
| Personality | configuration |

The Identity organ **exposes** these attributes on the privileged `agent` schema.
Their authority remains configuration unless the host intentionally changes them
(`assent_identity`, `speaker="assistant"` encode, or profile update).

## API

```python
CognitiveEngine(
    agent_id="aria",
    assistant_identity={
        "name": "Aria",
        "role": "cognitive assistant",
        "description": "…",
        "capabilities": ("memory", "planning"),
    },
)
```

Operational attributes are tagged `context_tags=("operational",)` and seeded at
schema ensure.

## Non-goals

- Not a new organ
- Not personality / consciousness
- Not automatic learning of the assistant’s name from user utterances or tool logs
