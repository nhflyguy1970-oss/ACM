# Teach vs Query Contract (B01)

**Status:** Normative  
**Module:** `acm.authority.teaching.detect_teaching`

## Utterance function

| Function | Detection | Pipeline effect |
|----------|-----------|-----------------|
| Declarative teach | Non-interrogative + Semantic Extraction yields facts | Encode before dispatch (`teaching_encoded`) |
| Interrogative query | `is_interrogative` | Never encodes; reconstruct only |
| Imperative / non-cognitive | No declarative facts | No teach; may be `not_memory` |

## Rules

1. Questions never teach — including preference, identity, goal, and project cues.
2. Teachings pass Trusted Memory Ingestion (D046); no host bypass.
3. Read-only diagnostic mode (B07) detects teachings but skips encode.
4. After a successful teach encode, dispatch reconstructs from the updated store.

## Examples

| Utterance | Teach? |
|-----------|--------|
| `My favorite color is blue.` | yes |
| `What is my favorite color?` | no |
| `My name is Jeff.` | yes |
| `Who am I?` | no |
| `Write a poem about fish.` | no |

## Validation

`tests/cognitive/test_preference_certification.py` ·
`tests/cognitive/test_teach_query_matrix.py`
