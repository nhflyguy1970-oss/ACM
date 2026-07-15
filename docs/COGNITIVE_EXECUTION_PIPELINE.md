# Cognitive Execution Pipeline

**Status:** Normative (v0.17.0)  
**Decisions:** D038 · D039 · D040

## Stages

| Step | Owner | Output |
|------|-------|--------|
| 1. Intent Classification | `classify_request` | `CognitiveIntent` + confidence |
| 2. Cognitive Ownership | `route_request` / ownership table | primary + supporting organs |
| 3. Dispatch | `CognitiveDispatchEngine` | organ invocation plan |
| 4. Organ execution | Organ handlers | `OrganContribution`s |
| 5. Merge / reconstruct | Dispatch merge | cognitive payload |
| 6. Gates | Memory Authority gates | status / strip ungrounded |
| 7. Result | `CognitiveMemoryResult` | structured product |
| 8. Speak | `speak_cognitive_result` | faithful language |

## Guarantees

- LM never classifies ownership or invents memory.
- Infrastructure never terminates cognition.
- Raw adaptation / store dumps are sanitized out of speech.
- User identity never answers as assistant identity.
