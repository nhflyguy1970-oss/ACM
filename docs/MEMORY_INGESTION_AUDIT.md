# Memory Ingestion Audit

**Repository:** standalone ACM reference implementation  
**Runtime inspected:** `01b0a43a16b059fbb619aaaa46d2c50a9f719a3c`  
**Certified code baseline:** `v0.18.4` /
`3023ed85b1de5a9b19c5058509f1fda870f45555`  
**Date:** 2026-07-17  
**Scope:** read-only source and runtime audit; documentation changes only

## Audit conclusion

Standalone ACM has one primary language-to-autobiographical-graph path:
`CognitiveEngine.encode`. `revise` and `reflect_on` are convenience entry
points into the same path. That path accepts arbitrary caller-provided text
unless a narrow speech-contamination marker rejects it. It does not require
proof that the content is a genuine user statement.

As a result, the following are incorrectly eligible for autobiographical
concept formation when passed to encode without a forbidden marker:

- tool outputs and tool execution status;
- internal diagnostics and debug output;
- memory-search responses;
- evidence reports and evidence-query wrappers;
- prompt fragments and system messages;
- assistant output or internal reasoning mislabeled as ordinary text;
- conversation-log rows regardless of speaker;
- host metadata serialized into text.

The engine does not autonomously read any of those sources. Eligibility becomes
contamination only when a host, adapter, utility, plugin, or import path submits
the material.

## Trust boundary

The public encode signature accepts:

- `text`
- cognitive `kind`
- `context_tags`
- `external_kind`
- optional `speaker`
- optional revision/reflection lineage

Of these:

- `speaker` changes semantic perspective but does not establish ingestion
  authority or survive as first-class provenance.
- `external_kind` describes medium, not trustworthy actor/source. It includes
  `conversation`, `terminal`, `filesystem`, and `other`.
- `context_tags` can reject known speech-generation markers, but protection
  depends on callers supplying them correctly.
- `kind` affects durability and concept roles but is not a source-security
  classification.

There is no required source field whose allowed value means “genuine user
knowledge.”

## Autobiographical creation and mutation paths

### 1. `CognitiveEngine.encode`

Location: `acm/api/engine.py::CognitiveEngine.encode`

This is the primary path that can create both Experiences and answerable
Concept attributes:

```text
reject_speech_contamination
  → infer_context
  → extract_semantics
  → attention/durability
  → ConceptOrgan.ingest_from_encode
  → ExperienceOrgan.birth
  → bind Experience to concepts/associations
  → IdentityOrgan.integrate_encode
  → provenance stamp
  → optional durable flush
```

Risk:

- arbitrary raw fallback text reaches concept cue extraction;
- caller metadata is advisory and incomplete;
- successful encode provenance is generically `origin=encode`.

### 2. `CognitiveEngine.revise`

Location: `acm/api/engine.py::CognitiveEngine.revise`

This delegates to `encode(..., revises_id=<experience>)`. It inherits all
encode eligibility and protection behavior. It can create new concepts and
attributes while preserving revision lineage.

### 3. `CognitiveEngine.reflect_on`

Location: `acm/api/engine.py::CognitiveEngine.reflect_on`

This host-supplied helper delegates to
`encode(..., reflects_on_id=<experience>, pin=True)`. Because it is an encode
path, host-supplied reflection text can form concepts and attributes. This is
distinct from the autonomous Reflection organ below.

### 4. Semantic Identity integration

Location: `acm/identity/organ.py::IdentityOrgan.integrate_encode`

Identity schemas are updated from facts extracted during encode. This is not an
independent language-ingestion entry point; it inherits encode's source trust.
Identity-specific collision and speaker protections do not constitute a
general tool/system source gate.

The existing test
`test_tool_outcome_kind_identity_no_assistant_user_name` explicitly encodes
`Tool memory_search worked for: My name is Jeff.` and checks only that assistant
identity does not absorb Jeff. It demonstrates that a tool outcome is accepted
by encode; it does not assert that the tool outcome is excluded from
autobiographical memory.

### 5. Autonomous Reflection

Location: `acm/reflection/organ.py::ReflectionOrgan`

`what_do_i_think` evaluates a reconstruction and directly births an immutable
Reflective Experience through `ExperienceOrgan`. It does not call
`CognitiveEngine.encode`, run concept cue extraction, or append concept
attributes.

Runtime evidence:

- reflection on fresh unknown preference memory created Reflective Experiences;
- concept count and provenance count did not grow;
- the subsequent preference query remained unknown.

Reflection can reinforce pre-existing concept IDs through later Learning, but
it did not create the reported text or preference attribute.

### 6. Learning

Location: `acm/learning/organ.py::LearningOrgan`

Learning consumes Reflective Experiences and writes governed Adaptation
records. It may adjust confidence/strength of existing concepts, associations,
preferences, identity concepts, or goals. It does not parse arbitrary tool text
into a new preference attribute.

Impact on contamination:

- it can strengthen or weaken an already contaminated concept if that concept
  becomes part of reflective evidence;
- it is not the origin of the reported value.

### 7. Reconsolidation

Location: `acm/remembering/organ.py::RememberingOrgan._reconsolidate`

Successful recall increments access, strength, confidence, accessibility, and
association weights. It does not create a new semantic attribute or replace its
value.

Impact on contamination:

- repeated successful recall can make an existing contaminated concept more
  likely to win later;
- it cannot originate `Tool memory_search worked for: ...`.

### 8. Reconciliation

Location: `acm/reconciliation/organ.py::ReconciliationOrgan`

Reconciliation creates Reconciliation records and may adjust confidence through
the Confidence organ. It explicitly checks that Experience chronology did not
change. It does not create preference attributes.

### 9. Experience-only births

The following paths create immutable Experiences without running semantic or
concept extraction:

- goal completion in `CognitiveEngine.complete_goal`;
- autonomous Reflection through `ExperienceOrgan.reflect`/`birth`;
- direct internal `ExperienceOrgan.birth` callers.

These records can participate as evidence but do not independently create the
reported generic preference concept.

Direct use of `ExperienceOrgan.birth` is an internal API and has no source
protection of its own.

### 10. Persistence import and startup load

Location: `acm/persistence/codec.py::import_store` and
`acm/persistence/sqlite.py`

Import reconstructs Experiences, Concepts, attributes, and provenance exactly
from a checksum-valid snapshot. It validates format/checksum compatibility, not
semantic source eligibility. A historically contaminated snapshot remains
contaminated after load.

Runtime evidence:

- the exact tool artifact encoded with auto-persistence produced the same known
  response before and after constructing a new engine on the same SQLite path.

### 11. Certification and trace utilities

Certification helpers and `identity.pipeline_trace` call the public encode API
with controlled test data. They are not automatic production ingestion paths,
but they demonstrate that any utility with engine access can create
autobiographical graph state.

### 12. Plugins

Current plugin hooks observe `after_encode` payloads. The core plugin protocol
does not itself initiate encode, but an external plugin or host retaining an
engine reference remains outside the standalone trust boundary and can call
the public API.

## Source eligibility findings

### Genuine user statement

Eligibility: accepted.  
Attribution quality: insufficient unless the host supplies and preserves
additional context. Default perspective assumes first person is the user, but
that is grammatical interpretation, not source proof.

### Assistant response

Eligibility: accepted if passed as ordinary `text`, `conversation`, `terminal`,
or `other`. Rejected only when the caller uses a forbidden external kind or
speech/assistant context tag.

### Tool output or execution status

Eligibility: accepted. `external_kind="terminal"` and unknown source kinds
normalized to `other` are allowed. The exact reported artifact reproduces.

### Internal diagnostics and debug output

Eligibility: accepted if passed to encode and durable by attention/kind/facts.
There is no diagnostic source category or textual rejection rule.

### Memory-search response

Eligibility: accepted. Neither `memory_search` nor a `Tool ... worked for:`
wrapper is protected. If the text mentions `favorite`, concept cue extraction
can promote it to a generic preference.

### Evidence query or evidence report

Eligibility: the read request itself is not automatically encoded by
standalone ACM. If a host logs it or its tool wrapper through encode, it is
accepted. `Show the evidence for my favorite color.` is also classified as a
preference request because evidence-introspection intent is deferred.

### System message or prompt fragment

Eligibility: accepted if passed to encode without forbidden tags. No system or
prompt source class exists.

### Assistant internal reasoning

Eligibility: accepted if serialized as ordinary text and passed to encode.
There is no content-independent actor/source gate.

### Reflection trace

Eligibility depends on path:

- autonomous Reflection births a Reflective Experience without concept
  extraction;
- host-supplied `reflect_on` delegates to encode and is therefore eligible to
  create concepts.

### Conversation log

Eligibility: accepted when rows are sent to encode. `external_kind` supports
`conversation`, but no required speaker role or turn type controls
autobiographical concept formation.

### Imported snapshot

Eligibility: accepted when schema/checksum validation passes. Semantic source
eligibility is not re-evaluated.

## Memory protection audit

Location: `acm/authority/protection.py::reject_speech_contamination`

Current positive protections:

- known language-model/speech context tags are rejected;
- known generated/speech external kinds are rejected;
- two obvious fabrication self-reports are rejected.

Observed runtime protection matrix for the exact tool artifact:

- default `external_kind="text"`: encoded;
- `external_kind="terminal"`: encoded;
- `external_kind="other"`: encoded;
- `external_kind="conversation"`: encoded;
- `external_kind="speech"`: rejected;
- `context_tags=("assistant_utterance",)`: rejected.

Gate failure:

The protection policy is a denylist for a subset of generated speech, not an
allowlist for autobiographical sources. It cannot reject an artifact whose host
metadata is absent, normalized, or semantically describes a medium rather than
an actor.

## Semantic extraction audit

`acm/semantic/extract.py`:

- preserves original input as evidence;
- strips only approved remember/note instructional phrases;
- defaults grammatical perspective to user when no speaker is supplied;
- sets `raw_fallback=true` when no structured facts match.

For the exact artifact, semantic fact extraction returns no facts. This stage
does not itself assert a preference. However, its unchanged `primary_summary`
feeds concept cue extraction.

`acm/concepts/extract.py`:

- enters preference handling whenever `prefer`, `favorite`, or `favourite`
  occurs anywhere in the text;
- if no declarative favorite pattern or `prefer <value>` pattern matches,
  creates `ConceptCue(label="preference", attr_key="preference",
  attr_value=<entire text>)`.

This is the direct semantic promotion error.

## Provenance audit

For the reproduced record:

- Experience provenance: `origin=encode`;
- winning Concept provenance: `origin=encode`, parented to Experience
  provenance;
- Experience metadata: exact evidence text, semantic-extraction marker,
  inferred first-person perspective;
- no source actor, tool name, message role, host operation, system/diagnostic
  classification, or reliable speaker attribution is retained.

Attribute evidence:

- the winning preference attribute carries the Experience ID;
- observed token-nucleus `mentioned` attributes do not carry attribute-level
  evidence IDs, though their concepts are associated with the Experience.

Therefore ACM can prove which Experience supports the winning attribute, but
cannot prove from structured provenance whether that Experience was a user
statement, tool output, assistant response, or system artifact. The verbatim
evidence text provides the only direct source clue in this incident.

## Rendering and authority audit

The response side behaves consistently with stored graph state:

- classification correctly recognizes a preference recall;
- routing correctly selects Remembering;
- D045 correctly excludes `mentioned`-only lexical concepts;
- the generic `preference` attribute is considered answerable under current
  rules;
- preference rendering faithfully formats its stored value;
- Memory Authority's confidence gate marks it known;
- speech returns known memory verbatim.

The response pipeline lacks an ingestion-source concept by design and cannot
repair source contamination after the fact. Rendering is the manifestation,
not the origin.

## Behavioral impact

- Internal infrastructure text can be asserted as user autobiography.
- A fresh user may receive a false known preference instead of unknown.
- Repeated ingestion strengthens the contaminated preference and can make it
  beat a genuine preference.
- Intermediate repetition can create a false semantic conflict despite D045's
  correct lexical filtering.
- Persistence makes the defect survive restart.
- Generic `origin=encode` can misleadingly make contaminated data look like
  ordinary encoded evidence.
- The same trust-boundary issue can affect Identity, Goals, Projects, and other
  semantic patterns when infrastructure text contains matching language.

## Recommended correction — not implemented

Subject to separate design approval:

1. Define a closed source taxonomy and require an autobiographical eligibility
   decision before language reaches semantic/concept extraction.
2. Default unknown, tool, system, diagnostic, prompt, generated, and assistant
   sources to non-autobiographical.
3. Preserve actor/source/operation metadata in durable provenance and on
   attribute lineage.
4. Require structured declarative preference extraction before creating a
   preference-role concept; raw fallback should remain evidence, not a
   preference value.
5. Audit host adapters separately to locate every encode caller and ensure only
   approved user knowledge crosses the boundary.
6. Add negative behavioral certification for every source category audited
   above.
7. Design explicit quarantine/remediation for historical contamination rather
   than silently deleting immutable Experiences.

No source, tests, behavior, architecture, persistence, or existing memory was
modified by this audit.
