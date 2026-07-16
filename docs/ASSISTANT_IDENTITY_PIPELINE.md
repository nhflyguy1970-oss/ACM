# Assistant Identity Pipeline

**Status:** Normative (v0.18.2)  
**Decision:** D043

## Request

`Who are you?` / `Tell me about yourself` / `What's your name?`

## Stages

```
Intent Classification → assistant_identity
        ↓
Perspective (n/a on recall; encode uses speaker/address rules)
        ↓
Ownership → Identity Organ (primary); no remembering fill for this intent
        ↓
Dispatch → terminate:identity
        ↓
Identity Organ → render_assistant_identity()
        ↓
Agent schema only (operational + structured agent attrs)
        ↓
Confidence = max(spoken attribute confidences) ≥ ~0.95 for operational name
        ↓
CognitiveMemoryResult (known)
        ↓
Faithful speech: "My name is Aria. My role is …"
```

## Encode rules (symmetric to user)

| Utterance | Subject |
|-----------|---------|
| `My name is Jeff.` (default / user speaker) | **User** |
| `kind=identity` alone | **User** first person (no flip) |
| `speaker="assistant"` | **Assistant** |
| `Your name is Aria.` / `You are Aria.` | **Assistant** (addressed) |
| Tool log containing `My name is Jeff.` | **User** (never assistant name) |

User-name → assistant collision is rejected unless `assent=True`.

## Trace checklist

At each stage verify: input, output, filtering, ranking, confidence, returned
record, reason selected. Assistant path must never select the user schema.
