# Identity Extraction

**Status:** Accepted (D041) · Companion to [`SEMANTIC_EXTRACTION.md`](SEMANTIC_EXTRACTION.md)

## Goal

Identity is stored as identity — structured attributes on user / assistant /
project schemas — never as raw utterances.

## Examples

| Utterance | Subject | Property | Value |
|-----------|---------|----------|-------|
| `My name is Jeff.` | User | name | Jeff |
| `I'm Jeff.` | User (conversational) | name | Jeff |
| `Call me Jeff.` | User | preferred_name | Jeff |
| `You are ARIA.` | Assistant | name | ARIA |
| `I am a research assistant.` + `speaker="assistant"` | Assistant | role | research assistant |
| `User's name is Jeff` | User | name | Jeff |

`kind=identity` alone does **not** select the assistant subject (D043).
Assistant self-encode requires `speaker="assistant"`.

## Instructional language

`Please remember that`, `don't forget`, `keep in mind`, etc. are stripped before
fact formation. They never appear in `Experience.summary` or attribute values.
They remain in evidence metadata only.

## Update semantics

| Prior | Later | Result |
|-------|-------|--------|
| User name = Jeff | User name = Jeffrey | Supersede → Jeffrey (no duplicate active name) |
| Assistant role = librarian | Assistant role = navigator | Propose (assent required) — unchanged policy |

User identity name / preferred_name / location / role revise in place.
Assistant self-identity conflicts still require assent (D009).

## Integration

`IdentityOrgan.integrate_encode(..., facts=...)` applies `CognitiveFact`s when
Semantic Extraction succeeds; otherwise falls back to legacy regex extraction.
