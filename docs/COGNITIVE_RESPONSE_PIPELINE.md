# Cognitive Response Pipeline

**Status:** Normative (v0.15.0)

## Flow

```text
User Request
    ↓
Intent Classification  (acm.authority.classification)
    ↓
Memory Request?
    ├─ NO  → status=not_memory (host may use LM for non-memory tasks)
    └─ YES
         ↓
    Route to ACM organ(s)
         ↓
    ACM Reconstruction (structured fields only as authority)
         ↓
    Evidence / confidence gate
         ↓
    CognitiveMemoryResult  (NOT generative NL authority)
         ↓
    Optional speak_cognitive_result (faithful templates)
         ↓
    Host may paraphrase ONLY the structured fields
```

## API

| Call | Role |
|------|------|
| `engine.classify_request(text)` | Classification dict |
| `engine.cognitive_respond(text)` | Full pipeline → public result |
| `engine.speak_cognitive_result(result)` | Faithful speech |

Implementation: `acm.authority.pipeline.CognitiveResponsePipeline`.

## Ordering rule

Language generation for memory content **SHALL NOT** precede ACM reconstruction.
If a host violates this order, the architecture is non-conformant (Supremacy Rule 1).

## Reasoning path

`reasoning_path` lists ACM stages (`classify_memory_request`, `route:*`, organ verb,
`gate:*`). It is **not** chain-of-thought and must not be shown as fabricated
inner monologue.
