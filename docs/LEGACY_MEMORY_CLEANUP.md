# Legacy Memory Cleanup (D047)

**Version:** v0.20.0  
**Decision:** D047 — Legacy Memory Contamination Cleanup  
**Scope:** standalone ACM only; not promoted into Aria without explicit approval

## Why legacy contamination exists

Before D046 (Trusted Memory Ingestion, v0.19.0), `CognitiveEngine.encode`
accepted any text an external caller supplied. Tool status wrappers,
diagnostic output, reflection traces, system messages, and infrastructure logs
could enter Semantic Extraction as ordinary conversation and become durable
Experiences, Concepts, and preference attributes
(`TOOL_ARTIFACT_CONTAMINATION_ANALYSIS.md`).

The investigation for D047 reproduced the full lifecycle on a genuine v0.18.4
engine:

- `encode("Tool memory_search worked for: …")` created a generic `preference`
  concept whose attribute value is the entire tool string.
- `encode("Diagnostic: my favorite color is probe-yellow.")` matched the
  declarative preference pattern and **superseded** the legitimate
  `favorite_color=blue` attribute on the shared preference concept — recall
  then answered `Your favorite color is probe-yellow.`
- Provenance for all of these records says only `origin=encode` with empty
  `source_actor`, `host_operation`, `message_role`, and `eligibility_reason`,
  because those fields did not exist before D046.

## Why D046 did not remove it

D046 is an ingestion gate. It rejects untrusted sources **before** Semantic
Extraction and intentionally never rewrites existing semantic memory.
Snapshots persisted before v0.19.0 restore their contaminated graph state
unchanged, and Reconstruction faithfully recalls what the graph contains.
Verified for v0.19.0/v0.20.0: `encode`, `revise_experience`, and `reflect_on`
are the only external ingestion paths and all evaluate the trust gate; there
is no live bypass. Remaining contamination is legacy data only.

## How the migration identifies contaminated memories

`acm.provenance.legacy_cleanup.cleanup_legacy_contamination(engine)` (also
`CognitiveEngine.cleanup_legacy_contamination()`) evaluates every Experience:

1. **D046-era records** (metadata contains `source_actor`): the recorded
   actor / host-operation / message-role is re-evaluated with the current
   `evaluate_ingestion` policy. Ineligible recorded sources are removed
   fail-closed (`recorded_source_ineligible:*`). This covers imported
   snapshots carrying fabricated or untrusted source metadata.
2. **Legacy external encodes** (metadata contains `semantic_extraction` but
   no `source_actor`): these predate the trust boundary, so their provenance
   alone would reject *everything*, including legitimate user memories. They
   are removed only when the original evidence text (metadata `evidence`,
   falling back to the summary) bears an affirmative non-user artifact
   signature (`legacy_untrusted_artifact:*`): tool wrappers, memory-search
   output, diagnostics, reflection traces, system messages, prompt fragments,
   infrastructure logs, or implementation metadata.
3. **Internal cognition** (no `semantic_extraction` metadata — Reflection
   organ births, goal-completion Experiences): never external ingestion,
   never touched.

## What removal does

For each contaminated Experience the migration removes:

- the Experience record, its runtime state, and temporal links touching it;
- Concepts whose entire evidence set was contaminated (e.g. the generic
  `preference` tool-string concept and artifact token nuclei), plus their
  associations, hierarchy edges, and working-buffer entries;
- attributes on surviving concepts that were created by the contaminated
  encode — matched through the contaminated record's extracted fact pairs
  (`fact_i_property`/`fact_i_value`) or verbatim payload text;
- provenance records of removed artifacts (valid provenance is preserved).

When a contaminated attribute superseded a legitimate one (D045-era attribute
versioning — the probe-yellow case), the newest surviving version of that key
is reactivated, restoring the user's taught value.

## Why legitimate memories are preserved

- Legacy memories without an affirmative artifact signature are presumed
  legitimate user knowledge: the artifact classifier is conservative and
  first-person user statements ("My favorite color is blue.", "My wife's
  name is Sarah.") can never match it.
- Identity, preference, and relationship concepts keep their clean evidence;
  only contaminated lineage entries are stripped.
- Contamination judgments key on provenance-era metadata and original
  evidence text, never on how "useful" a memory looks.

## Idempotency

Running the migration on an already-clean graph removes nothing and mutates
nothing (verified by persistence checksum equality in
`tests/cognitive/test_legacy_memory_cleanup.py`). Repeated runs after a
cleanup are no-ops because the contaminated records no longer exist and D046
prevents new ones from forming.

## Validation

`tests/cognitive/test_legacy_memory_cleanup.py` runs against
`tests/fixtures/pre_d046_contaminated_snapshot.json`, a genuine snapshot
produced by ACM v0.18.4 (commit `3023ed8`) containing four legitimate user
memories and five accepted artifacts. It verifies:

- contaminated recall reproduces before migration (probe-yellow);
- no current encode path bypasses the trust gate;
- migration removes exactly the five artifacts with correct classifications;
- blue preference, Jeff identity, Sarah relationship, and the journal memory
  survive; recall answers `Your favorite color is blue.`;
- valid provenance is preserved and no dangling provenance remains;
- idempotency (checksum-equal second run) and clean-graph no-op;
- teach-after-cleanup works; repeated tool-artifact injection cannot
  recreate contamination; D046 still rejects missing/unknown provenance;
- fabricated D046 metadata is removed fail-closed;
- internal cognition Experiences are never removed;
- the cleanup flushes the durable store and survives restart.
