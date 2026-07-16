# Identity Rendering Pipeline

**Status:** Normative (v0.18.3)  
**Decision:** D044

## Who am I?

```
Intent: user_identity
  → Identity organ render_user_identity()
  → User attributes only (name, preferred_name, …)
  → isolate_identity_text(target=user)
  → CognitiveMemoryResult.memory
  → speak_cognitive_result (verbatim)
```

Example: `Your name is Jeff. You prefer to be called Jeffrey.`

## Who are you?

```
Intent: assistant_identity
  → Identity organ render_assistant_identity()
  → Operational / agent attributes only
  → isolate_identity_text(target=assistant, forbid user values)
  → CognitiveMemoryResult.memory
  → speak_cognitive_result (verbatim)
```

Example: `My name is ARIA. My role is assistant.`

Never: `I'm ARIA, and you know me as Jeff.`

## Stage checklist

At every stage verify: identity selected, data retrieved, supporting evidence,
renderer inputs, filtering, final result, speech — **only** the requested identity.
