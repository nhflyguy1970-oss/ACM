# Semantic Extraction

**Status:** Accepted (D041) · **Version:** v0.18.0  
**Scope:** Standalone ACM only — not promoted into Aria until explicit approval.

## Principle

The language model understands language. ACM understands cognition.

Natural language is translated into **structured cognitive facts** before any organ
stores information. Organs receive cognitive facts. Raw conversational wording is
retained only as **supporting evidence**.

```
Natural Language
      ↓
Semantic Extraction   (acm.semantic)
      ↓
Structured Cognitive Facts
      ↓
Owning Cognitive Organ
      ↓
Memory Formation
```

## Properties

| Property | Guarantee |
|----------|-----------|
| LM-independent | Pure deterministic patterns — no model calls |
| Host-independent | No Aria / Jarvis / provider imports |
| Provider-independent | No OpenAI / Ollama / cloud APIs |
| Language-forward | Pattern set is extensible for future languages |

## Insertion point

`CognitiveEngine.encode()` — after D046 Trusted Memory Ingestion eligibility,
speech-contamination protection, and context inference, **before** Concept /
Experience / Identity organ storage. Rejected sources never reach this module.

## API

```python
from acm.semantic import extract_semantics

result = extract_semantics(
    "My name is Jeff. Please remember that.",
    kind="experience",
    speaker=None,  # optional: "user" | "assistant"
)
# result.facts → CognitiveFact list
# result.evidence → original wording
# result.primary_summary → authoritative cognitive phrasing for Experience.summary
```

`encode(..., speaker=...)` accepts an optional speaker hint for hosts that know
who is talking. `speaker` controls grammatical perspective, not source trust;
every encode also requires an eligible `IngestionProvenance`.

## Packages

| Module | Role |
|--------|------|
| `acm.semantic.model` | `CognitiveFact`, `ExtractionResult`, enums |
| `acm.semantic.strip` | Remove instructional / meta language |
| `acm.semantic.perspective` | Resolve I/you → user/assistant/third party |
| `acm.semantic.facts` | Pattern extractors |
| `acm.semantic.extract` | Orchestrator |

## Companions

- [`IDENTITY_EXTRACTION.md`](IDENTITY_EXTRACTION.md)
- [`PERSPECTIVE_RESOLUTION.md`](PERSPECTIVE_RESOLUTION.md)
- [`COGNITIVE_FACT_MODEL.md`](COGNITIVE_FACT_MODEL.md)
- [`FACT_EXTRACTION_RULES.md`](FACT_EXTRACTION_RULES.md)
