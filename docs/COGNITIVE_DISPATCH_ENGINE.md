# Cognitive Dispatch Engine

**Status:** Normative (v0.17.0)  
**Decision:** D040  
**Module:** `acm.authority.dispatch`

## Problem

Classification (D039) and Memory Authority (D038) are necessary but not
sufficient. Correct intent does not guarantee correct **execution**. Cognitive
requests must never terminate in implementation infrastructure or return raw
storage dumps as answers.

## Rule

ACM owns **complete end-to-end cognitive dispatch**.

```text
User Request
  → Intent Classification
  → Cognitive Ownership
  → Dispatch
  → Owning Organ (+ Supporting Organs)
  → Cognitive Reconstruction
  → CognitiveMemoryResult
  → Faithful Language Rendering
```

Only this pipeline may answer cognitive questions.

## Cognitive Termination Rule

A cognitive request SHALL terminate ONLY at a cognitive organ.

It shall NEVER terminate at MemoryStore, MemoryEngine, KnowledgeEngine,
SearchEngine, database, index, vector store, cache, provider, language model,
or storage.

`CognitiveStore` may appear only as **substrate** (`infrastructure_role:
substrate_only`).

## API

```python
engine.dispatch_request(text)   # ownership + organ execution diagnostics
engine.cognitive_respond(text)  # full pipeline → CognitiveMemoryResult
```

## Diagnostics

Results include `diagnostics` with: intent, primary_organ, supporting_organs,
dispatch_path, reconstruction_path, terminated_at, contributions, confidence,
provenance count, uncertainty, infrastructure_role.

## Related

- [`COGNITIVE_EXECUTION_PIPELINE.md`](COGNITIVE_EXECUTION_PIPELINE.md)
- [`COGNITIVE_HANDLER_MODEL.md`](COGNITIVE_HANDLER_MODEL.md)
- [`ORGAN_OWNERSHIP_VALIDATION.md`](ORGAN_OWNERSHIP_VALIDATION.md)
- [`INFRASTRUCTURE_ABSTRACTION.md`](INFRASTRUCTURE_ABSTRACTION.md)
