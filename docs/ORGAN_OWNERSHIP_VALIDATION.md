# Organ Ownership Validation

**Status:** Normative (v0.17.0)  
**Suite:** `tests/cognitive/test_cognitive_dispatch.py`

## Verified routes

| Request | Intent | Terminates at |
|---------|--------|---------------|
| Who are you? | `assistant_identity` | Identity |
| Who am I? | `user_identity` | Identity (user path) |
| What projects are we working on? | `project` | Remembering (+ Experiences, Concepts, Identity, Goals) |
| What is our long-term goal? | `goal` | Goals (+ Remembering, Identity, Experiences) |
| How has your understanding changed? | `reflection` | Reflection (+ Learning, Experiences, Remembering) |
| How are these related? | `association` | Associations |
| What have you learned? | `learning` | Learning |
| What do you remember? | `remembering` | Remembering |

Every cognitive result exposes `diagnostics.terminated_at` equal to the
primary organ. Infrastructure names never appear as terminals.
