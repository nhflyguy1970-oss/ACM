# Preference Editing UX — B11

**Status:** Implemented (ACM v0.37.0)

## Purpose

Explicit, explainable preference view / preview / propose / assent / reject /
cancel / apply over existing semantic encode + attribute supersede.

## APIs

| API | Role |
|-----|------|
| `inspect_preferences` / `inspect_preference` | Read-only list / lineage |
| `preview_preference_change` | Old→new without write |
| `propose_preference_change` | Pending assent |
| `assent_preference_change` / `reject` / `cancel` | Gate resolution |
| `apply_preference_change` | Trusted-host commit (`assent=True`) |

Commits always birth Experiences via `encode()`; never mutate Experience history.
Remove deactivates the living attribute after recording removal Experience.

## Validation

Cognitive / behavioral / learning (L27) suites.
