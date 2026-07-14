# Developer Guide

## Setup

```bash
cd /path/to/ACM
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check acm tests
```

## Layout

```
acm/
  api/           # Public CognitiveEngine
  types/         # Enums, Attribute, EnvelopeRef
  core/          # CognitiveStore (in-memory substrate)
  identity/      # M1 Identity organ + Policy Gate
  experiences/   # M2 Experience organ (immutable events, timeline)
  concepts/      # M3 Concept organ (nuclei, hierarchy, prototypes)
  plugins/       # Extension registry (non-core capabilities)
  attention/     # Attention classification
  context/       # Context frames
  working/       # Working buffer
  validation/    # Validation harness
  observability/ # Cognitive traces
  …              # Later milestone organs
docs/            # Constitution, architecture, plugins, boundaries, API
tests/
  unit/
  behavioral/
  cognitive/
  performance/
examples/
```

## Rules of engagement

1. **Independence** — never import Aria, Mission Control, Capability Bus, AI-Platform, or Conversation Trace.
2. **Cognition first** — justify changes against `MEMORY_DESIGN_PRINCIPLES.md`.
3. **Emergence** — do not hard-code identity, preferences, or confidence scripts.
4. **Boundaries** — see `CORE_BOUNDARIES.md`; extensions use `PLUGIN_ARCHITECTURE.md`.
5. **Observability** — cognitive state changes should land in ValidationHarness / TraceLog.
6. **Deviations** — record in `DECISION_LOG.md`; do not silently rewrite architecture.

## Adding a milestone slice

1. Read Principles § relevant + Architecture organ + Test Strategy contracts.
2. Implement the smallest behavior that proves the cognitive claim.
3. Add unit + behavioral + cognitive tests.
4. Update API / ROADMAP / CHANGELOG / DECISION_LOG as needed.
5. Commit; ensure CI green before the next slice.

## Running the hello example

```bash
python examples/hello_acm.py
```
