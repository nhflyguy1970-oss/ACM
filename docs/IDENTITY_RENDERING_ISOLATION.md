# Identity Rendering Isolation

**Status:** Normative (v0.18.3)  
**Decision:** D044

## Rule

Identity responses are composed **only** from the identity being requested.

| Question | Allowed source | Forbidden |
|----------|----------------|-----------|
| Who am I? | User schema only | Assistant profile, assistant memories, operational attrs |
| Who are you? | Assistant operational / agent schema only | User name, preferences, projects, goals, history |

Cross-identity content is allowed **only** for explicit relationship questions
(e.g. “What have you learned about me?”, “Describe our relationship.”).

## Enforcement layers

1. `render_user_identity()` / `render_assistant_identity()` — structured attrs only  
2. `isolate_identity_text()` — sentence filter + foreign-value ban  
3. Pipeline `_materialize` — `identity_render_isolate` before `CognitiveMemoryResult`  
4. `speak_cognitive_result` — final identity intent pass  

## Banned blend forms

- `you know me as …`
- `I am known as <user name>`
- `and you are / while you are …`
- User second-person on assistant answers
- Assistant first-person on user answers
