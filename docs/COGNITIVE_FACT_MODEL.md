# Cognitive Fact Model

**Status:** Accepted (D041)

## Definition

A **CognitiveFact** is the authoritative unit Semantic Extraction produces:

| Field | Meaning |
|-------|---------|
| `kind` | identity · preference · goal · project · relationship · location · possession · skill · experience · correction · negation · teachable |
| `subject` | user · assistant · third_party · shared · unknown |
| `property` | e.g. name, preferred_name, role, location, favorite_coffee |
| `value` | Structured value (never instructional wording) |
| `relation_type` | Optional (dog, friend, …) for relationships |
| `confidence` | Extraction confidence |
| `update_op` | set · revise · negate · strengthen |

## Authority

- Structured fact = authoritative cognitive content  
- Original language = supporting evidence only (`Experience.metadata["evidence"]`)  
- `Experience.summary` = `canonical_summary()` from facts (or cleaned text if no facts)

## ExtractionResult

Bundles `facts`, `evidence`, `perspective`, `instructional_stripped`, `raw_fallback`,
and `primary_summary`.
