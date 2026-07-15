# Memory Authority Model

**Status:** Normative (v0.15.0)  
**Decision:** D038  
**Rule:** Memory is a cognitive task. The language model is never memory authority.

## Core claim

Autobiographical recall, identity, experiences, learning residual, concepts,
associations, goals, preferences, confidence judgments, and reconciliation
results are produced **only** by ACM organs.

A language model (any host LLM) may **communicate** an ACM result in natural
language. It may **never**:

- invent memories
- complete missing memories
- reconstruct memory
- guess autobiographical facts
- overwrite ACM uncertainty
- become an Experience / Concept / Association / Reflection by itself

## Sole authority

| Capability | Authority |
|------------|-----------|
| Encode lived/taught events | ACM `encode` (+ protection gates) |
| Reconstruct “what do I remember?” | ACM Remembering (+ Memory Authority pipeline) |
| Identity | ACM Identity / `who_am_i` |
| Learning residual | ACM Learning |
| Reflection | ACM Reflection |
| Confidence / uncertainty | ACM Confidence |
| Reconciliation | ACM Reconciliation |
| Surface speech of a memory answer | `speak_cognitive_result` templates **or** host LM constrained to the structured result |

## Host contract

1. Classify or call `CognitiveEngine.cognitive_respond(request)`.  
2. If `is_memory_request` is true, **do not** call an LLM for factual content first.  
3. After ACM returns a `CognitiveMemoryResult`, speech may occur **only** by expressing that result.  
4. Never encode LLM utterances as Experiences (`memory_protection` rejects speech/LM tags).

## Unknown is knowledge

Statuses `unknown`, `insufficient_evidence`, `low_confidence`, and `conflicting`
are valid cognitive outcomes. Faithful speech must communicate them — never
fabricate fillers.

## Related docs

- [`COGNITIVE_RESPONSE_PIPELINE.md`](COGNITIVE_RESPONSE_PIPELINE.md)  
- [`MEMORY_CLASSIFICATION.md`](MEMORY_CLASSIFICATION.md)  
- [`HALLUCINATION_PREVENTION.md`](HALLUCINATION_PREVENTION.md)  
- [`UNKNOWN_MEMORY.md`](UNKNOWN_MEMORY.md)  
- [`MEMORY_PROTECTION.md`](MEMORY_PROTECTION.md)  
- [`COGNITIVE_MEMORY_OBJECT.md`](COGNITIVE_MEMORY_OBJECT.md)
