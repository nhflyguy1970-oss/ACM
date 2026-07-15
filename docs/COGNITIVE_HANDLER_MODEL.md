# Cognitive Handler Model

**Status:** Normative (v0.17.0)  
**Module:** `acm.authority.handlers`

## Model

Each cognitive organ is invoked through a **handler** that returns an
`OrganContribution`:

- `organ` — terminator name (cognitive vocabulary only)
- `memory` — **cognitive speech text**, never raw dict/records
- `confidence`, evidence lists, reconstruction steps
- `substrate_touched` — informational only (`cognitive_store`, `context_frame`)

## Forbidden terminals

Handlers refuse termination at: `memory_store`, `memory_engine`,
`knowledge_engine`, `search_engine`, `database`, `index`, `vector_store`,
`cache`, `provider`, `language_model`, `storage`, etc.

## Formatting rules

- Learning adaptations are summarized into human cognitive language.
- User-identity reconstruction uses user schema + biography cue; assistant
  first-person bleed (`I am {agent}`) is stripped.
- Dict-/JSON-shaped answers are rejected by `sanitize_cognitive_text`.
