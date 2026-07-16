# Identity Pipeline Trace

**Status:** Accepted (D042) · **Version:** v0.18.1  
**Scope:** Standalone ACM only

## Exact example

```
Who am I?  →  low_confidence (empty user schema)
My name is Jeff.
Who am I?  →  Your name is Jeff.
```

## Stage evidence (post-fix)

| Stage | Arrived? | Notes |
|-------|----------|-------|
| Natural language | yes | `My name is Jeff.` |
| Semantic Extraction | yes | Fact: identity / user / name / Jeff (0.93) |
| Perspective Resolution | yes | first_person=user (`conversational_default_user`) |
| Structured Cognitive Fact | yes | `User name is Jeff` canonical summary |
| Identity Organ input | yes | facts list passed to `integrate_encode` |
| Identity Organ storage | yes | status=`adopted` on user schema |
| Database representation | yes | Experience.summary=`User name is Jeff`; evidence metadata retains original |
| Identity structured record | yes | Subject=user · Property=name · Value=Jeff · Confidence=0.92 |
| Remembering retrieval | yes | `_user_identity` reads structured attributes |
| Confidence calculation | yes | **0.92** from name attribute (not schema 0.4) |
| CognitiveMemoryResult | yes | status=`known`, memory=`Your name is Jeff.` |
| Faithful language rendering | yes | `Your name is Jeff.` |

## Defect found (pre-fix)

1. Concept cue extraction on summary `User name is Jeff` matched the privileged **user** schema label and wrote `mentioned=user` onto identity attributes.
2. `_user_identity` rendered **all** attributes (`mentioned: user. Your name is Jeff.`) and used **schema.confidence** (~0.4–0.56) instead of the name attribute confidence (0.92).
3. Near-threshold schema confidence produced unstable / low-confidence answers in behavioral validation.

## Fix (implementation only)

- Skip applying `mentioned`/`statement`/`category` cues onto identity schema concepts.
- `_user_identity` speaks only structured keys (name, preferred_name, role, location, capability, clean statement) and uses **max(attribute confidence)**.

## Observable API

```python
from acm import CognitiveEngine
from acm.identity import trace_identity_pipeline

report = trace_identity_pipeline(CognitiveEngine(agent_id="aria"))
assert report["ok"]
```
