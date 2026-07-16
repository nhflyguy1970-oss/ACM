# Identity Context Filtering

**Status:** Normative (v0.18.3)  
**Decision:** D044

## Prevented on simple identity questions

| Leak class | Example | Action |
|------------|---------|--------|
| Automatic personalization | “and you know me as Jeff” | Drop |
| Context merging | Assistant + user attrs in one answer | Drop foreign side |
| Conversation blending | History injected into identity | Not used |
| Identity blending | `I am known as <user>` | Drop |
| Memory blending | Remembering gap-fill (already blocked D043) | Blocked |
| Cross-entity references | “while you are …” | Drop |

## Allowed only when explicit

- How do we know each other?
- What have we worked on together?
- What have you learned about me?
- Describe our relationship.

Detected by `is_relationship_identity_request()`.

## Module

`acm.identity.rendering` — `isolate_identity_text`, forbidden-value helpers.
