# Cognitive Routing

**Status:** Normative (v0.16.0)  
**Module:** `acm.authority.routing`  
**API:** `CognitiveEngine.route_request` · `CognitiveRoutingEngine`

## Purpose

After Cognitive Intent Classification, the **Cognitive Routing Engine** assigns
exactly one primary cognitive owner and optional supporting organs, then
invokes those organs. The language model never selects the organ.

```text
User Request
  ↓
Intent Classification
  ↓
Determine Cognitive Owner
  ↓
Route ONLY to owning organ (+ supports)
  ↓
CognitiveMemoryResult
```

## Routing examples

| Request | Intent | Primary | Supports |
|---------|--------|---------|----------|
| Who are you? | `assistant_identity` | Identity | — |
| Who am I? | `user_identity` | Identity | — |
| What projects are we working on? | `project` | Remembering | Experiences, Concepts, Identity, Goals |
| What is our long-term goal? | `goal` | Goals | Remembering, Identity, Experiences |
| How has your understanding changed? | `learning` | Learning | Remembering |
| What do you remember about fly tying? | `remembering` | Remembering | Experiences, Concepts |
| How are these related? | `association` | Associations | Concepts, Remembering |
| What have you learned? | `learning` | Learning | Remembering |

## Engine API

```python
engine.route_request("Who am I?")
# → classification + ownership (no reconstruction yet)

engine.cognitive_respond("Who am I?")
# → full classify → route → reconstruct → CognitiveMemoryResult
```

## Coordination

Primary organ produces the candidate reconstruction. Supporting organs may
contribute evidence (project schema, active goals, relational edges). Final
authority remains `CognitiveMemoryResult` under Memory Authority gates.

**Identity exception (D043):** `user_identity` and `assistant_identity` have
**no** supporting organs. Identity is the sole speech authority for
`Who am I?` / `Who are you?`. Remembering must never gap-fill those answers.
