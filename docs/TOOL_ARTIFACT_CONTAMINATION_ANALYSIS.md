# Tool Artifact Contamination Analysis

**Repository:** standalone ACM reference implementation  
**Runtime inspected:** `01b0a43a16b059fbb619aaaa46d2c50a9f719a3c`
(code-equivalent to certified `v0.18.4` / `3023ed85b1de5a9b19c5058509f1fda870f45555`;
`01b0a43` changes documentation only)  
**Date:** 2026-07-17  
**Scope:** diagnostic investigation only; no correction implemented

## Finding

The reported response reproduces on a fresh standalone engine when the exact
tool status text is passed to the public encode API:

```python
engine.encode(
    "Tool memory_search worked for: "
    "Show the evidence for my favorite color."
)
```

The result is:

```text
Your preference is Tool memory_search worked for:
Show the evidence for my favorite color..
```

The defect is an ingestion-boundary failure followed by an extraction false
positive:

1. An external caller invokes `CognitiveEngine.encode` with internal tool status
   text. Standalone ACM contains no producer for the phrase
   `Tool memory_search worked for:`; repository search found it only as literal
   test input. The tool wrapper therefore entered from outside standalone ACM.
2. `reject_speech_contamination` permits the input when it is untagged or marked
   as `text`, `conversation`, `terminal`, or `other`. It has no tool-result,
   diagnostic, system, or infrastructure source class and does not recognize
   this wrapper.
3. Semantic fact extraction correctly finds no structured fact, but returns the
   unchanged text as `primary_summary` with `raw_fallback=true`.
4. Concept cue extraction treats any text containing `favorite` as preference
   material. Because the text does not match the declarative
   `favorite <property> is <value>` form, it falls back to a generic
   `preference` attribute whose value is the entire tool status string.
5. D045 correctly regards that attribute as semantic: its key is not lexical
   metadata, and its value neither starts with an interrogative nor ends in `?`.
   D045 cannot infer that a declarative tool wrapper contains an embedded
   question.
6. Remembering activates and selects the generic preference concept. The
   preference renderer faithfully renders the contaminated value. Memory
   Authority then marks the grounded, sufficiently confident reconstruction
   `known`, and the speech layer returns it verbatim.

The renderer did not invent the text. Reflection, reconsolidation, and
reconciliation did not create the attribute. The attribute was created during
the original external encode.

## Complete reconstruction trace

### 1. User query

Input:

```text
What is my favorite color?
```

### 2. Intent classification

`acm/authority/classification.py::classify_memory_request` matches
`preference_cue`:

- `is_memory_request=true`
- `intent=preference`
- `confidence=0.93`
- `ownership_hint=remembering`

The separate query `Show the evidence for my favorite color.` also matches
`preference_cue`. This known, deferred lack of an evidence-introspection intent
is documented as B02, but classification alone does not encode either query and
did not create this contamination.

### 3. Ownership and dispatch

`acm/authority/routing.py` assigns:

- primary organ: `remembering`
- supporting organ: `experiences`
- rationale: preferences are reconstructed as remembered experiences

`acm/authority/dispatch.py` invokes Remembering first and terminates at
Remembering. Infrastructure remains substrate-only.

### 4. Cue extraction and activation

`acm/activation/engine.py::ActivationEngine._collect_seeds` derives query tokens
from the lower-case whitespace split:

```text
what, favorite, color?
```

Substring matching lets `color?` match the stored artifact value's `color.`.
The generic preference concept receives:

- a lexical seed from label `preference` where applicable;
- question energy because `favorite` and `color?` occur in the attribute value;
- strength, attention, accessibility, and working-memory modulation.

Repeated encoding or recall can strengthen this concept. In a controlled
five-run matrix, one artifact encode was always enough to win in an otherwise
fresh graph. With a valid blue preference also present, one artifact did not
beat blue; three repeated artifacts produced a conflict and five repeated
artifacts made the tool artifact the winner. The graph state therefore controls
which answer wins, but the result is deterministic for a fixed graph.

### 5. Candidate memories

The artifact encode creates eight concepts:

- `preference` / role `preference` /
  `preference="Tool memory_search worked for: Show the evidence for my favorite color."`
- `tool` / role `entity` / `mentioned="tool"`
- `memory_search` / role `entity` / `mentioned="memory_search"`
- `worked` / role `entity` / `mentioned="worked"`
- `show` / role `entity` / `mentioned="show"`
- `evidence` / role `entity` / `mentioned="evidence"`
- `favorite` / role `entity` / `mentioned="favorite"`
- `color` / role `entity` / `mentioned="color"`

D045 excludes the seven `mentioned`-only concepts from answerability and
ambiguity scoring. That behavior is correct. The generic `preference` concept
remains answerable because its non-lexical attribute contains query tokens.

### 6. Winning concept

The winner in the fresh reproduction is:

```text
label: preference
role: preference
attribute key: preference
attribute value: Tool memory_search worked for:
                 Show the evidence for my favorite color.
active: true
attribute confidence: 0.70
```

The reconstruction is non-ambiguous, has explanation class `preference`, and
crosses the known-answer confidence gate.

### 7. Supporting evidence and attribute origin

The winning attribute has exactly one evidence ID. It resolves to an Experience
with:

```text
summary: Tool memory_search worked for:
         Show the evidence for my favorite color.
external_kind: text
cognitive_kind: observation
metadata.evidence: same tool status string
metadata.semantic_extraction: "1"
metadata.perspective_first: "user"
```

Encoding the same text with `kind="preference"` changes only the Experience
cognitive kind to `preference`; the false preference concept is also created
with the default `kind="experience"`. Mislabeling the encode kind is therefore
not required for reproduction.

Attribute-source attribution:

- The generic `preference` value originates verbatim from the external encode
  argument through `ConceptCue.attr_value`.
- The seven `mentioned` values originate from tokenization of that same encode
  argument.
- No value originates from assistant rendering, Reflection, Learning,
  Reconciliation, Reconsolidation, or persistence.
- The Experience and winning concept provenance records both say only
  `origin=encode`. The Experience record preserves the exact text but not a
  trustworthy actor/source class.
- Token-nucleus attributes have no attribute-level evidence IDs in the observed
  graph. This limits direct provenance attribution, though their values and
  creation path are deterministic from the same input.

### 8. Renderer and final response

`acm/remembering/organ.py::_format_from_concept` sees a preference-role concept
and renders:

```text
Your preference is <attribute value>.
```

`acm/authority/pipeline.py` gives the result status `known`.
`acm/authority/speak.py` returns known memory text verbatim. The doubled final
period is the stored value's period plus the preference template's period.

## Where the artifact entered the graph

The earliest demonstrated graph mutation is:

```text
external caller
  → CognitiveEngine.encode(tool status text)
  → reject_speech_contamination allows input
  → extract_semantics returns raw fallback
  → concepts.extract.extract_cues generic preference fallback
  → ConceptOrgan creates preference attribute
  → ExperienceOrgan stores exact evidence
  → persistence retains graph
```

Standalone ACM does not automatically ingest conversations, tool results,
system messages, or Memory Authority responses. A call to `cognitive_respond`,
including an evidence query, does not call `encode`. Therefore the original
production event necessarily involved an external caller invoking `encode`,
`revise`, `reflect_on`, or importing an already contaminated snapshot. The
observed provenance (`origin=encode`) rules out import for the reproduced event
and is consistent with direct encode/revise/reflect-on entry. The exact stored
summary most strongly identifies a host-generated tool execution status as the
payload.

The standalone record cannot identify the external caller or distinguish
direct `encode` from the two helpers because ACM does not persist caller,
operation, actor, or message-role provenance. Locating the concrete host call
site would require a separate host-repository audit, which is outside this
standalone-only investigation. What is proven here is the complete
standalone-side path from an externally supplied tool artifact to the rendered
false preference, including the exact failed gates.

## Memory Authority audit

Memory Authority correctly owns and terminates the recall request, but its
current ingestion protection is not a complete source-authority gate.

It rejects:

- explicitly forbidden external kinds: `llm`, `language_model`, `speech`,
  `generated`, `completion`;
- context tags such as `assistant_utterance`, `speech_output`,
  `host_generation`, and `chat_completion`;
- two explicit self-reported fabrication phrases.

It accepts:

- untagged tool output;
- `external_kind="terminal"`;
- `external_kind="conversation"`;
- `external_kind="other"`;
- diagnostics, evidence reports, system/prompt fragments, and internal metadata
  when callers present them through ordinary encode without forbidden tags.

No source-eligibility check establishes that the input is genuine user
knowledge. Intent classification is a response-routing gate and is not invoked
by `encode`.

## Reproduction matrix

- **Fresh autobiographical memory, query only:** unknown; no Experience,
  Concept, or provenance growth.
- **Fresh memory, evidence query only:** unknown; no autobiographical growth.
- **Fresh memory, exact artifact encoded once:** known contaminated preference;
  deterministic in repeated runs.
- **After restart:** contamination persists and reproduces identically from the
  durable snapshot.
- **After diagnostics/read-only inspection:** no contamination; standalone
  inspection does not encode.
- **After evidence query:** no contamination unless an external host records its
  tool/status response through encode.
- **After Reflection:** Reflection births Reflective Experiences, including on
  unknown memory, but the tested reflection path created no new concepts or
  attributes and did not create the tool artifact.
- **With an existing valid blue preference:** one artifact remained secondary;
  repeated artifact ingestion eventually competed and then won.

Classification of the incident:

- **Historical:** yes, once stored and persisted.
- **Live:** yes, the current encode boundary still accepts the payload.
- **Deterministic:** yes for a fixed graph and sequence.
- **Apparently intermittent:** only because activation strength, repetition,
  valid competing preferences, attention, and working-memory state vary.

## Defect boundary

Primary defect:

- **ACM ingestion/source authority:** tool and infrastructure artifacts are
  eligible for ordinary autobiographical encode unless a cooperative caller
  supplies one of a small set of forbidden speech markers.

Secondary defect:

- **Concept cue extraction:** a mere occurrence of `favorite` is promoted to a
  preference concept, and unmatched syntax stores the entire input as the
  preference value.

Contributing observability defect:

- **Provenance:** `origin=encode` does not distinguish user statement, tool
  output, assistant response, system message, diagnostic output, or prompt
  artifact. `speaker` influences perspective but is not retained as
  authoritative source provenance.

Not the source:

- Memory Authority response classification or dispatch;
- D045 lexical answerability filtering;
- Reflection;
- Learning;
- Reconciliation;
- Reconsolidation;
- persistence serialization;
- final rendering.

## Recommended correction — not implemented

Any correction requires separate approval and certification. The narrowest
defensible correction should combine:

1. A closed ingestion-source contract that distinguishes user knowledge from
   tool results, assistant speech, system messages, diagnostics, prompts,
   traces, and generated evidence reports. Non-user infrastructure sources
   should be ineligible for autobiographical concept formation by default.
2. Enforcement inside `CognitiveEngine.encode`, not only in host code, so
   omitted or normalized metadata cannot silently downgrade a tool result to
   ordinary text.
3. Preference concept creation only from an extracted declarative preference
   fact (or another explicitly approved teaching contract), never from keyword
   occurrence plus raw-text fallback.
4. Durable source provenance on Experiences and attributes, including actor,
   source class, host operation, and transformation lineage.
5. Negative certification covering tool wrappers, diagnostics, search
   responses, evidence requests/reports, system prompts, assistant output,
   internal reasoning, and imported contaminated snapshots.
6. A separately approved remediation plan for already persisted contaminated
   records; this investigation does not delete or rewrite history.

No correction, migration, architecture change, or behavioral change was made
during this investigation.
