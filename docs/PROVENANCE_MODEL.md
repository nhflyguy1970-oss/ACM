# Provenance Model — ACM

**Status:** Canonical for Phase 2 (P2.2)  
**Rule:** Never fabricate provenance.

## Cognitive / engineering question

*Where did this artifact originate? Which observed memories contributed?*

This is **traceability engineering**, not a new cognitive organ.

## Origins

`told` · `perceived` · `inferred` · `reconstructed` · `legacy_import` · `learned` · `reflective` · `reconciled` · `simulated` (contributor only) · `analogical` · `encode` · `unknown`

## Record fields

Artifact kind/id · origin · contributor / experience / learning / reflection / reconciliation / simulation / analogy / confidence event ids · parent provenance ids · explain · `fabricated=false`

## Stamping

`encode` stamps Experience + Concept provenance from **observed** ids only.  
Adapter shadow writes may stamp `legacy_import`.

## API

`CognitiveEngine.provenance_of(artifact_id)` → public records.

## Observability

ValidationHarness `provenance` aggregate (`acm.validation/0.13`).
