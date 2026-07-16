# Perspective Resolution

**Status:** Accepted (D041)

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
| `kind="identity"` without teaching cues | Assistant | User |
| Conversational default | User | Assistant |

## Never confuse

- User teaching “My name is Jeff” → **user** schema  
- Assistant self-encode “I am a research assistant” (`kind=identity`) → **agent** schema  
- “You are ARIA” → **assistant** schema  

## API

`acm.semantic.perspective.resolve_perspective(text, kind=..., speaker=...)`
