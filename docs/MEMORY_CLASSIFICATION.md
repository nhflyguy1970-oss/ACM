# Memory Classification

**Status:** Normative (v0.15.0)  
**Module:** `acm.authority.classification`

## Purpose

Decide whether an inbound utterance requires cognitive memory **before** any
language-model generation.

## Outcomes

| `is_memory_request` | `intent` | Host obligation |
|---------------------|----------|-----------------|
| true | `identity`, `remembering`, `learning`, … | Call ACM pipeline first |
| false | `not_memory` | Non-memory task; LM allowed for generation (still cannot become memory) |

## Covered intents

Identity · Experience · Remembering · Reflection · Learning · Concept ·
Association · Goal · Preference · Confidence · Reconciliation · Project ·
History · Autobiography · Pattern · General memory.

## Signals (examples)

- “Who are you?” / “Who am I?” → identity  
- “What do you remember…?” / “What is my …?” → remembering  
- “What have you learned?” → learning  
- “What happened…?” → experience  
- “Write a poem…” → not_memory  

Classification is host-agnostic regex/heuristic routing inside ACM. Hosts may
add richer NLP **before** calling ACM, but must not replace ACM reconstruction.
