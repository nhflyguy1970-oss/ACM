# Identity Separation

**Status:** Normative (v0.18.2)  
**Decision:** D043

## Rule

**User Identity** and **Assistant Identity** are separate cognitive entities.

They shall never:

- resolve to each other
- overwrite one another
- share active identity attributes (especially `name`)

| Question | Intent | Schema |
|----------|--------|--------|
| Who am I? | `user_identity` | `user` |
| Who are you? | `assistant_identity` | `agent` |

## Operational vs autobiographical

| Kind | Schema | Source |
|------|--------|--------|
| Autobiographical | `user` | Lived / taught conversation |
| Operational | `agent` | Configuration (`assistant_identity` / `agent_id`) |

## Dispatch integrity

For `user_identity` and `assistant_identity`, supporting organs must **not** fill
memory gaps. Gap-fill from remembering was a contamination path that surfaced
operational assistant names as answers to `Who am I?`.

## Validation

See `tests/cognitive/test_assistant_identity_separation.py`.
