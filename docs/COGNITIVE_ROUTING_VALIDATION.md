# Cognitive Routing Validation

**Status:** Normative (v0.16.0)  
**Suite:** `tests/cognitive/test_cognitive_intent_routing.py`  
**Regression:** `tests/cognitive/test_memory_authority.py`

## Coverage

| Area | Gate |
|------|------|
| Identity questions | Parametrized matrix + pipeline `who_am_i` / user identity |
| Autobiographical | Autobiography classification |
| Experience / remembering | Matrix + encode/recall path |
| Reflection / learning / confidence | Ownership + intent asserts |
| Goal / project | Intent + pipeline |
| Association / concept | Ownership routes |
| Preference / history / decision | Classification matrix |
| Reasoning / planning / tools / knowledge | Non-cognitive asserts |
| Mixed / ambiguous | Self-referent conservation |
| Unknown | Unicorn unknown remains unknown |
| Host independence | Pure `classify_memory_request` without store |
| False routing | Poem / translate → not_memory |
| Hallucination prevention | Memory Authority speak checks |
| Memory Authority preservation | `allow_encode_from_speech=False` |
| Performance | Batch classify bound |
| Regression | Full `tests/cognitive/` |

## Critical invariants

1. `Who are you?` ≠ `Who am I?` (assistant vs user identity).
2. Project / goal / learning questions are `is_memory_request=True`.
3. LM never owns cognitive questions.
4. Uncertain self-referent questions remain cognitive-conservative.

## Run

```bash
pytest tests/cognitive/test_cognitive_intent_routing.py tests/cognitive/test_memory_authority.py -q
```
