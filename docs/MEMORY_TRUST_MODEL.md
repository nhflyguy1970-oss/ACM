# Memory Trust Model

**Decision:** D046  
**Version:** `trusted_memory_ingestion.v1`  
**Scope:** external autobiographical ingestion

## Principle

Long-term autobiographical memory is a privileged destination.

Content is not trusted because it resembles a fact, contains first-person
language, arrives in conversation, carries high attention, or was supplied by a
host. It is trusted only when the ingestion request explicitly identifies an
eligible source.

Unknown provenance fails closed.

## Trust declaration

`IngestionProvenance` is a non-cognitive control record. It has exactly three
required dimensions.

### Actor

The actor identifies who supplied the content:

- `user`
- `assistant`
- `tool`
- `system`
- `reflection`
- `diagnostic`
- `memory`
- `planner`
- `scheduler`
- `conversation`
- `infrastructure`
- `unknown`

Only `user` is eligible under D046.

### Host operation

The operation identifies how the content entered:

- `conversation`
- `encoding`
- `retrieval`
- `reflection`
- `tool_execution`
- `memory_search`
- `diagnostic`
- `system_event`
- `unknown`

Only `conversation` and `encoding` are eligible, and only in combination with
an eligible user actor and role.

### Message role

The role identifies the submitted message:

- `user_statement`
- `user_teaching`
- `user_correction`
- `assistant_reply`
- `tool_result`
- `reflection_output`
- `diagnostic_output`
- `system_message`
- `prompt_text`
- `metadata`
- `conversation_text`
- `infrastructure_log`
- `unknown`

Only the three explicit user roles are eligible.

## Eligibility rule

An ingestion request is eligible if and only if:

```text
actor == user
AND host_operation IN {conversation, encoding}
AND message_role IN {user_statement, user_teaching, user_correction}
```

All other combinations reject.

The decision reason is stored as one of:

- `trusted_user_statement`
- `trusted_user_teaching`
- `trusted_user_correction`

Rejected requests report a bounded reason such as:

- `missing_provenance`
- `unknown_actor`
- `unknown_host_operation`
- `unknown_message_role`
- `actor_not_autobiographical`
- `host_operation_not_eligible`
- `message_role_not_eligible`

## Fail-closed behavior

Trust evaluation is the first encode operation. A rejected request must not:

- infer or mutate conversational context;
- invoke Semantic Extraction;
- allocate cognitive attention;
- create or reinforce Concepts;
- create Experiences;
- update Identity, Preference, Goals, or Projects;
- create associations;
- alter confidence, priority, accessibility, or working memory;
- stamp accepted-memory provenance;
- flush a changed snapshot.

The rejection result is operational evidence only:

```json
{
  "encoded": false,
  "reason": "memory_trust",
  "detail": "actor_not_autobiographical",
  "ingestion": {
    "eligible": false,
    "reason": "actor_not_autobiographical",
    "provenance": {
      "actor": "tool",
      "host_operation": "memory_search",
      "message_role": "tool_result"
    },
    "schema": "trusted_memory_ingestion.v1"
  }
}
```

This rejection object is not stored as cognitive content.

## Provenance invariant

Every Experience created by the public external encode path has enough durable
metadata to answer:

1. Who supplied it?
2. How did it enter ACM?
3. What role did the message have?
4. Why was it eligible?

The accepted Experience and primary Concept provenance records carry the four
answers. The Experience metadata mirrors them so attribute evidence IDs can be
followed to the source declaration.

The source fields never participate in:

- semantic fact values;
- Concept attributes;
- cue matching;
- activation energy;
- confidence scoring;
- reconstruction;
- user-facing rendering.

They are audit controls, not cognition.

## Trust is independent of content

The policy intentionally does not inspect wording to decide source identity.

- A tool result containing `My favorite color is blue` remains a tool result.
- A system prompt containing `My name is Jeff` remains a system message.
- An assistant reply containing a true user fact remains an assistant reply.
- A user statement remains eligible even when Semantic Extraction ultimately
  finds no durable fact or attention declines to store it.

Hosts are responsible for truthful source declarations. ACM is responsible for
rejecting every declared non-user source and every missing/unknown declaration.

The existing speech/LM contamination checks remain as defense in depth against
incorrectly classified generated content.

## Operational identity

Assistant identity is not learned from assistant replies. It remains
operational configuration established by `agent_id` and `assistant_identity`.

Trusted user statements may still describe or address the assistant, and the
existing `speaker` perspective hint remains available. Actor trust and semantic
perspective are separate dimensions.

## Internal cognition boundary

D046 governs external content presented for autobiographical encode.

Existing internal organs may continue to create bounded cognitive artifacts
through their established APIs:

- Reflection creates Reflective Experiences;
- Learning creates Adaptation records;
- Reconciliation creates Reconciliation records;
- Reconsolidation updates accessibility and confidence;
- goal completion records its established Experience.

Those internal artifacts do not become trusted external user statements. If a
host serializes any internal output and submits it to `encode`, it must declare
the true non-user source and ACM rejects it.

## Persistence and compatibility

The source fields are additive to provenance and Experience metadata.
Schema-v1 snapshots without D046 fields remain readable; missing fields on
historical records remain empty rather than being fabricated.

The encode API is intentionally fail-closed and therefore behaviorally
breaking for callers that omit provenance. v0.19.0 reflects that host contract
change. Hosts must migrate every external encode call before promotion.

No trusted default may be configured by an adapter on behalf of an unknown
caller.

## Non-goals

D046 does not implement:

- teach-versus-query intent recognition;
- evidence-query intent or evidence presentation;
- read-only diagnostics;
- provenance presentation UX;
- preference editing/correction UX;
- source confidence weighting;
- rich scientific source monitoring;
- historical contamination deletion;
- automatic host-call-site discovery.

Those remain separate decisions. D046 is only the trust boundary required to
prevent untrusted external content from entering semantic autobiographical
memory.
