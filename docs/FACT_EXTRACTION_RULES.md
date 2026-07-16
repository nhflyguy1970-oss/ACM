# Fact Extraction Rules

**Status:** Accepted (D041)

## What is extracted structurally

| Domain | Triggers (examples) | Fact |
|--------|---------------------|------|
| Identity name | my name is / I'm ProperName / call me / you are / user's name | identity.name / preferred_name |
| Role | I am a/an … | identity.role |
| Skill | I can … | skill.capability |
| Relationship | my dog's/cat's/… name is | relationship.name + relation_type |
| Location | I live in / I'm from / based in | location.location |
| Preference | I prefer / favorite X is | preference.* |
| Goal | my goal is / I want to | goal.goal |
| Project | my project is / working on | project.project |
| Correction | actually, my name is | identity revise |
| Negation | my name is not | identity negate |

## False extraction prevention

- Weather / filler / non-identity chatter → `raw_fallback` (no invented identity)
- `I'm ready` / `I'm sorry` → not treated as personal names (roleish filter)
- Relationship possessives never become user name
- Name tokens stop at sentence boundaries (no spill across clauses)

## Ambiguity

When no pattern matches, ACM does **not** invent facts. Experience may still encode
cleaned text as observational content with evidence retained.
