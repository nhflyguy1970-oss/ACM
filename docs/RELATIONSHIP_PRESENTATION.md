# Relationship-Memory Presentation — B21

**Status:** Implemented (ACM v0.41.0)  
**Depends on:** B19 · B29 · D044

## Purpose

Safely answer explicit user↔assistant relationship questions using stored
evidence — without leaking into simple identity answers.

## APIs

| API | Role |
|-----|------|
| `cognitive_respond("How do we know each other?")` | Conversational path |
| `present_relationship_memory(request)` | Direct read-only presentation |

Detected by `is_relationship_identity_request()`. Classification routes these
cues to Remembering (not Learning dump / not_memory).

## Isolation

| Cue | Behavior |
|-----|----------|
| Who are you? | Assistant schema only |
| Who am I? | User schema only |
| How do we know each other? / Describe our relationship / What have you learned about me? | Relationship presentation allowed |

Never invents Experiences. Never writes the store.

## Validation

Cognitive / behavioral / learning (L31) / long-duration suites.
