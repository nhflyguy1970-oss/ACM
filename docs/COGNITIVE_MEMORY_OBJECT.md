# Cognitive Memory Object

**Status:** Normative (v0.15.0)  
**Schema:** `cognitive_memory_result.v1`

## Type

`acm.authority.result.CognitiveMemoryResult`

## Fields

| Field | Role |
|-------|------|
| `status` | Authority status (`known` / `unknown` / …) |
| `is_memory_request` | Classifier outcome |
| `intent` | Routed memory intent |
| `memory` | Propositional ACM content (null when not known) |
| `confidence` | ACM confidence |
| `uncertainty` | Named uncertainty label |
| `explanation_class` | Remembering explanation class |
| `provenance` | Provenance public rows for supporting artifacts |
| `supporting_experiences` | Experience ids/summaries |
| `supporting_concepts` | Concept ids |
| `supporting_associations` | Association ids |
| `reflective_evidence` | Reflection outcomes when applicable |
| `learning_evidence` | Learning adaptations/lessons |
| `reasoning_path` | ACM pipeline stages |
| `ambiguous` | Competing recollections |
| `language_may_speak` | Speech allowed after ACM |
| `allow_encode_from_speech` | Always `false` |

## Public API

`CognitiveEngine.cognitive_respond` → `result.to_public()` dict.

This object is the **only** approved cognitive payload for memory questions.
Natural language is a presentation of this object — never its source.
