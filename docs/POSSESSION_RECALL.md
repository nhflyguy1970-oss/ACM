# Adjacent Possession / Relationship Recall — B47

**Status:** Implemented (ACM v0.43.0)  
**Depends on:** B21 · Semantic Extraction relationship facts

## Purpose

Answer possession/relationship name cues (e.g. “What's my dog's name?”) from
stored relationship facts **without** polluting `Who am I?` / `Who are you?`.

## APIs

| API | Role |
|-----|------|
| `cognitive_respond("What's my dog's name?")` | Conversational path |
| `present_possession_recall(request)` | Direct read-only recall |

## Isolation

| Cue | Behavior |
|-----|----------|
| Who am I? | User schema only (no pet names) |
| What's my dog's name? | Relationship fact → Zeus |

## Validation

Cognitive / behavioral / learning (L33) / long-duration suites.
