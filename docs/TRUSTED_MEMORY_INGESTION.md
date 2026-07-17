# Trusted Memory Ingestion

**Decision:** D046  
**Release:** v0.19.0  
**Status:** Implemented in standalone ACM only  
**Date:** 2026-07-17

## Problem

ACM previously accepted arbitrary host text through `CognitiveEngine.encode`.
The speech-contamination denylist rejected correctly tagged language-model
output, but untagged tool, system, diagnostic, retrieval, and infrastructure
messages remained eligible.

The failure was demonstrated by encoding:

```text
Tool memory_search worked for:
Show the evidence for my favorite color.
```

Because the content reached concept formation as ordinary text, its mention of
`favorite` produced an answerable preference attribute. Reconstruction and
rendering then correctly exposed the already-contaminated value.

## Correction

D046 adds a source-eligibility decision at the start of
`CognitiveEngine.encode`, before context inference, Semantic Extraction,
attention allocation, Concept formation, Experience birth, Identity
integration, or provenance mutation.

Every encode request now supplies an `IngestionProvenance` containing:

- actor — who supplied the content;
- host operation — how the content entered ACM;
- message role — what kind of message it is.

Missing, unknown, inconsistent, or non-user provenance is rejected by default.
A rejected request returns a structured `memory_trust` result and creates no
Experience, Concept, attribute, association, provenance record, or durable
snapshot change.

## Public API

```python
from acm import CognitiveEngine, TRUSTED_USER_TEACHING

engine = CognitiveEngine()
result = engine.encode(
    "My favorite color is blue.",
    kind="preference",
    provenance=TRUSTED_USER_TEACHING,
)
assert result["encoded"] is True
```

Hosts that need an operation-specific declaration construct it explicitly:

```python
from acm import CognitiveEngine
from acm.provenance import (
    HostOperation,
    IngestionActor,
    IngestionProvenance,
    MessageRole,
)

source = IngestionProvenance(
    actor=IngestionActor.USER,
    host_operation=HostOperation.CONVERSATION,
    message_role=MessageRole.USER_STATEMENT,
)
engine = CognitiveEngine()
engine.encode("My name is Jeff.", provenance=source)
```

Tool output is explicitly rejected:

```python
tool_source = IngestionProvenance(
    actor=IngestionActor.TOOL,
    host_operation=HostOperation.MEMORY_SEARCH,
    message_role=MessageRole.TOOL_RESULT,
)
rejected = engine.encode(
    "Tool memory_search worked for: My name is Jeff.",
    provenance=tool_source,
)
assert rejected["encoded"] is False
assert rejected["reason"] == "memory_trust"
```

## Accepted sources

The closed D046 policy accepts only these combinations:

- actor `user`;
- host operation `conversation` or `encoding`;
- message role `user_statement`, `user_teaching`, or `user_correction`.

Convenience constants are immutable source declarations:

- `TRUSTED_USER_STATEMENT`
- `TRUSTED_USER_TEACHING`
- `TRUSTED_USER_CORRECTION`

They do not bypass policy. They represent the three approved user roles.

## Rejected sources

The following are ineligible for autobiographical semantic encoding:

- assistant replies and assistant operational metadata;
- tool results and tool-execution status;
- system messages and prompt fragments;
- diagnostic output and debug traces;
- memory-search and retrieval results;
- reflection output presented as external content;
- planner and scheduler output;
- infrastructure logs and implementation metadata;
- generic conversation text without a user-statement role;
- any missing or unknown provenance.

Media classification such as `text`, `terminal`, `conversation`, or `other`
does not grant trust. `external_kind` continues to describe the medium; it is
not the source-authority decision.

## Actor and speaker are different

`IngestionProvenance.actor` identifies who supplied the content to ACM and is
used for eligibility. The existing optional `speaker` hint resolves grammatical
first/second-person perspective during Semantic Extraction.

A trusted user can supply a statement about the assistant while the semantic
speaker hint remains `assistant`. Conversely, marking an assistant reply with
`speaker="user"` does not make the source eligible. Trust is determined only
from the explicit ingestion declaration.

Assistant operational identity remains configuration-driven through
`agent_id`/`assistant_identity`; assistant output is not autobiographical
input.

## Processing order

```text
encode request
  → trusted-ingestion decision
  → legacy speech/LM contamination defense
  → context inference
  → Semantic Extraction
  → attention and durability
  → Concept / Experience / Identity integration
  → source-aware provenance
  → optional persistence
```

This order is an invariant. Semantic Extraction never receives rejected
content.

## Provenance recording

Accepted Experience and primary Concept provenance now record:

- `source_actor`
- `host_operation`
- `message_role`
- `eligibility_reason`

The supporting Experience metadata records the same bounded fields. Source
metadata is audit-only; it is not included in Experience summaries, Concept
labels, semantic attributes, activation cues, or rendered answers.

The original `origin=encode` lineage remains unchanged for compatibility.
Older persisted provenance records load with empty D046 fields; new records
always contain the accepted source decision.

## Related ingestion helpers

`revise_experience` and host-supplied `reflect_on` now accept and forward an
explicit `provenance` argument. The compatibility adapter accepts
`ingestion_provenance` for shadow encoding and no longer manufactures a trusted
default.

Autonomous cognitive Reflection, Learning, Reconsolidation, and Reconciliation
remain internal organ behavior. D046 does not add an organ or change their
architecture. External reflection/diagnostic text submitted through encode is
rejected.

## Architectural invariants preserved

D046 does not change:

- Cognitive Intent Classification;
- Cognitive Routing or Dispatch;
- Memory Authority response ownership;
- Semantic Extraction patterns;
- Identity or Preference integration rules;
- Activation or Reconstruction;
- D045 answerability and competitor admissibility;
- rendering or faithful speech;
- immutable Experience chronology;
- existing cognitive organs.

The correction changes only whether external content may reach those existing
systems.

## Validation

`tests/cognitive/test_trusted_memory_ingestion.py` certifies:

- missing and unknown provenance reject before Semantic Extraction;
- tool, memory-search, reflection, diagnostic, prompt, system, metadata,
  infrastructure, and assistant sources create zero autobiographical state;
- repeated rejected artifacts cannot displace a genuine preference;
- genuine user identity, relationship, and preference knowledge still encodes;
- source metadata persists through SQLite restart;
- assistant operational identity remains available through configuration.

All D038–D045 behavioral suites remain active and now supply explicit trusted
user provenance for their encode requests.

## Promotion boundary

D046 exists only in standalone ACM v0.19.0. It is not active in Aria or any
vendored ACM copy until a separate controlled promotion is approved.
