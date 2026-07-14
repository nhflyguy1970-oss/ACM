# Dependency Rationale

## Runtime

**None** (stdlib only) for `aria-cognitive-memory` core.

Rationale: plug-and-play cognitive engine; minimal host friction; no forced vector DB / ML stack.

## Development (`[dev]`)

| Package | Why |
|---------|-----|
| `pytest` | Unit / behavioral / cognitive tests |
| `pytest-cov` | Coverage for milestone gates |
| `ruff` | Fast lint consistent with modern Python |

Future optional extras (vector indexes, embedding providers, multimodal codecs) must remain *optional* and never required to `encode` / `remember` text experiences.
