# Perspective Resolution

**Status:** Accepted (D041) · Aligned with D043

## Problem

Pronouns are ambiguous without conversational perspective:

- **I / me / my / mine** may mean the user or the assistant
- **You / your / yours** usually addresses the other party

Confusing user identity with assistant identity is a cognitive defect.

## Resolution rules

| Signal | First person | Second person |
|--------|--------------|---------------|
| `speaker="user"` | User | Assistant |
| `speaker="assistant"` | Assistant | User |
| Explicit user referent (`user's name`, `the user is`) | User | Assistant |
| Remember / teaching instruction (`please remember`) | User | Assistant |
| Conversational default | User | Assistant |

**`kind="identity"` does not flip first person to assistant.** Assistant
self-encode requires an explicit `speaker="assistant"` (D043). Bare
`kind=identity` is treated as conversational user autobiography.

## Never confuse

- User teaching “My name is Jeff” → **user** schema
- Assistant self-encode “I am a research assistant” (`speaker="assistant"`) → **agent** schema
- “You are ARIA” → **assistant** schema

## API

`acm.semantic.perspective.resolve_perspective(text, kind=..., speaker=...)`
