# Question Classification

**Status:** Normative (v0.16.0)  
**Companion:** [`COGNITIVE_INTENT_CLASSIFICATION.md`](COGNITIVE_INTENT_CLASSIFICATION.md)

## Quick map (operator reference)

| Question | Intent | Cognitive? |
|----------|--------|------------|
| Who are you? / Tell me about yourself | `assistant_identity` | Yes |
| Who am I? / What is my name? | `user_identity` | Yes |
| What do you know about me? | `autobiography` | Yes |
| What projects are we working on? | `project` | Yes |
| What is our long-term goal? / What is our plan? | `goal` | Yes |
| How has your understanding changed? | `learning` | Yes |
| What do you remember about X? | `remembering` | Yes |
| How are A and B related? | `association` | Yes |
| What do you think about X? | `reflection` | Yes |
| How certain are you? | `confidence` | Yes |
| What is my favorite …? | `preference` | Yes |
| What happened …? | `experience` | Yes |
| What did we decide …? | `decision_history` | Yes |
| Write a poem / translate / install | `procedural` / `general_knowledge` | No |
| Help me plan a vacation | `planning` | No |
| Hello / thanks | `conversation_management` | No |
| What is the speed of light? | `general_knowledge` | No |

## Ambiguous / mixed

Self/shared referents with cognitive verbs → cognitive-conservative
(`general_memory` / `uncertain`), **not** LM ownership.

## Host duty

1. Call `classify_request` or `cognitive_respond` for every user turn that may
   be cognitive.
2. If `is_memory_request` is true → do not answer from LM memory invention.
3. Speak only via `speak_cognitive_result` for cognitive results.
