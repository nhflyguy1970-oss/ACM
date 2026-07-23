# Memory Classification

**Status:** Normative (superseded in detail by v0.16 Cognitive Intent Classification)  
**Module:** `acm.authority.classification`  
**See:** [`COGNITIVE_INTENT_CLASSIFICATION.md`](COGNITIVE_INTENT_CLASSIFICATION.md) · [`QUESTION_CLASSIFICATION.md`](QUESTION_CLASSIFICATION.md)

## Purpose

Decide whether an inbound utterance requires cognitive memory **before** any
language-model generation, and which **cognitive intent** applies.

## Outcomes

| `is_memory_request` | `intent` | Host obligation |
|---------------------|----------|-----------------|
| true | cognitive intents (`assistant_identity`, `remembering`, `goal`, …) | Call ACM pipeline first |
| false | non-cognitive (`procedural`, `general_knowledge`, `not_memory`, …) | Host may generate; still cannot become memory |

## Covered intents (v0.16)

Identity (assistant/user) · Autobiography · Experience · Remembering ·
Reflection · Learning · Concept · Association · Goal · Preference ·
Confidence · Reconciliation · Project · History · Decision history ·
Working memory · Current context · Pattern · General memory · Uncertain ·
plus classified non-cognitive surfaces.

## Critical examples

- “Who are you?” → `assistant_identity` → Identity Organ (sole speech authority)
- “Who am I?” → `user_identity` → Identity Organ (sole speech authority; no remembering fill) 
- “What projects are we working on?” → `project` → Remembering (+ supports)  
- “What is our long-term goal?” → `goal` → Goals  
- “How has your understanding changed?” → `learning` → Learning  
- “Write a poem…” → `procedural` → not memory  

Classification is host-agnostic inside ACM. Hosts must not replace ACM
reconstruction or organ ownership.
