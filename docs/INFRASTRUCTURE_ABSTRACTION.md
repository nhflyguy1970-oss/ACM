# Infrastructure Abstraction

**Status:** Design finding + minimal implementation (v0.17.0)  
**Decision:** D040

## Research finding

Cognitive organs historically read CognitiveStore (substrate) and return
organ verbs. The Daily Use failure mode was not primarily “store exists”, but
**terminal leakage**:

1. Host layers (MemoryStore / MemoryEngine / Knowledge) answering instead of
   ACM organs (integration issue; ACM must still refuse to be that endpoint).
2. Learning organ returning **raw adaptation records** as if they were speech.
3. User-identity path recalling assistant `who_am_i` content via cue bleed.

## Abstraction stance (this correction)

| Layer | Role |
|-------|------|
| Cognitive organ handlers | Sole cognitive terminals |
| CognitiveStore / persistence | Substrate only (`infrastructure_role=substrate_only`) |
| Host MemoryStore / KnowledgeEngine / Search | Outside ACM authority; never ACM terminals |
| Language model | Speak only via `speak_cognitive_result` |

A full remapping of all organs onto a new abstract substrate API is **deferred**.
Required for D040: termination validation, handler sanitization, multi-organ
dispatch, and diagnostics that never name infrastructure as authority.

## Implemented

- `FORBIDDEN_TERMINALS` guard in dispatch
- Cognitive speech sanitization (no dict dumps; strip assistant bleed for user identity)
- Diagnostics list substrate as support only
