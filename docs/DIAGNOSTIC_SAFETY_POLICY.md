# Diagnostic Safety Policy — B09

**Status:** Implemented (ACM v0.35.0)  
**Depends on:** B07 read-only mode · B08 inspect façades · B29 redaction

## Purpose

Define what diagnostic output may expose and which operations/fields are
forbidden. Composes B29 privacy redaction; never invents Experiences; never
mutates living memory.

## Policy (production default)

| Setting | Default |
|---------|---------|
| `enabled` | `True` (opt-out only for explicit development) |
| Redaction | B29 `STRICT` |
| Strip `organ_payload.raw` | Yes |
| Strip `reconstruction_steps` | Yes |
| Sanitize `substrate_touched` | Map store names → `substrate_only` |
| List caps | provenance/experiences ≤ 20; concepts/assoc ≤ 12 |

Configure:

```python
CognitiveEngine(diagnostic_safety_policy=DiagnosticSafetyPolicy(...))
```

## Surfaces

- `inspect()` (B07) — now policy-gated at projection boundary
- All B08 façades (`inspect_*`)
- `organ_view` / `organ_views` (B27)

Payloads include `safety_policy`, `safety_policy_enabled`, `safety_policy_applied`.

## Forbidden

Raw store dumps, `memory_store` / DB rows, stack traces, module paths,
cross-identity bleed (via B29), infrastructure terminals as cognitive authority.

## Non-goals

- Conversation-safe capture UX (B10)
- Legal erase (B36)
- Host Trace UI

## Validation

- `tests/cognitive/test_diagnostic_safety_policy.py`
- `tests/behavioral/test_diagnostic_safety_conversation.py`
- Learning gate L25
