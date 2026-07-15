# Cognitive Intent Classification

**Status:** Normative (v0.16.0)  
**Decision:** D039  
**Module:** `acm.authority.classification` · `acm.authority.taxonomy`

## Problem

Memory Authority (D038) correctly prevents language models from inventing memory.
Daily Use testing showed a second flaw: the request classifier was too shallow.
Autobiographical and cognitive questions (projects, goals, self-introduction,
understanding change) were misclassified as general language and could bypass
the cognitive pipeline.

## Architectural rule

**Every inbound request SHALL first pass Cognitive Intent Classification.**

Classification determines whether the request is cognitive and **which organ
owns the answer**. The language model never determines cognitive ownership.

```text
User Request
    → Cognitive Intent Classification
    → Cognitive Ownership (Routing)
    → Owning organ reconstructs
    → CognitiveMemoryResult
    → Faithful speak (optional)
```

## Outputs

| Field | Meaning |
|-------|---------|
| `is_memory_request` | True → Memory Authority must run before LM speech |
| `intent` | `CognitiveIntent` value |
| `confidence` | Classification confidence |
| `uncertain` | True when specialized intent is not clear |
| `ownership_hint` | Primary organ hint (confirmed by Routing) |
| `schema` | `cognitive_intent_classification.v1` |

## Uncertain classification

If intent cannot be specialized confidently:

1. **Do not** silently route ownership to the language model when self/shared
   referents (`I`/`you`/`we`/`our`) plus cognitive signals are present.
2. Assign `GENERAL_MEMORY` or `UNCERTAIN` with `is_memory_request=True`.
3. Route to Remembering (conservative default).
4. Apply uncertainty caps so weak reconstructions do not become `known`.

Bare world-knowledge interrogatives without self/cognitive cues may remain
non-cognitive (`GENERAL_KNOWLEDGE`) with `uncertain=True`.

## Independence

Classification is host-, model-, provider-, and plugin-independent. It uses
deterministic linguistic cues inside ACM only.

## Related

- [`INTENT_TAXONOMY.md`](INTENT_TAXONOMY.md)
- [`COGNITIVE_ROUTING.md`](COGNITIVE_ROUTING.md)
- [`COGNITIVE_OWNERSHIP.md`](COGNITIVE_OWNERSHIP.md)
- [`QUESTION_CLASSIFICATION.md`](QUESTION_CLASSIFICATION.md)
- [`MEMORY_AUTHORITY_MODEL.md`](MEMORY_AUTHORITY_MODEL.md)
