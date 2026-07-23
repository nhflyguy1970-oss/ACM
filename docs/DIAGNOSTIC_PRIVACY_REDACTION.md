# Diagnostic Privacy & Redaction (B29)

**Status:** Implemented (M4 AML C1)  
**Scope:** Diagnostic projection boundary only — inspect façades and organ views.

## Rule

Explainability surfaces must never leak unrelated identity, context, or sensitive
content. Cognitive answers remain governed by D044 conversational isolation;
diagnostics reuse the same primitives at the read-model boundary.

## Policy

| Level | Behavior |
|-------|----------|
| `strict` (default) | Identity isolation + email/phone scrub + snippet bounds; fail-closed |
| `standard` | Same filters; may emit `[redacted]` instead of omitting |
| `none` | Passthrough (development / explicit override) |

Configure via `CognitiveEngine(redaction_policy=RedactionPolicy(...))`.

## Surfaces

- `inspect_reconstruction` / `inspect_evidence` / `inspect_confidence` /
  `inspect_identity` / `inspect_conflict`
- `organ_view` / `organ_views`

Each payload includes `redaction` and `redaction_applied`.

## Non-goals

- Host diagnostic UX (B10)
- Legal erase flows (B36)
- Mutating memory or inventing evidence

## Companion

- B09 field allow/deny and forbidden surfaces: [`DIAGNOSTIC_SAFETY_POLICY.md`](DIAGNOSTIC_SAFETY_POLICY.md)

## Architectural constraints

- Memory Authority absolute — redaction never replaces reconstruction
- No raw store dumps
- Learning may reorganize memory later but must never invent memory
