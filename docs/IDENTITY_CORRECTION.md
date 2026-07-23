# Identity Correction & Assent UX — B20

**Status:** Implemented (ACM v0.40.0)  
**Depends on:** B01 · B19 · IdentityPolicyGate

## Purpose

Make identity changes explicit, reviewable, and reversible under the existing
Policy Gate — without weakening user/assistant isolation.

## APIs

| API | Role |
|-----|------|
| `preview_identity_change` / `propose_identity_change` | Preview / pending |
| `assent_identity` / `reject_identity` / `cancel_identity` | Gate resolution |
| `apply_identity_change` | Trusted-host commit |
| `preview_identity_correction` / `apply_identity_correction` | Conversational |
| `pending_identity_changes` | Read-only pending list |

Commits use `encode(kind='identity', assent=True)`. Collision of user names onto
assistant schema is blocked. Correction lineage is a side-channel (Experiences
are frozen).

## Validation

Cognitive / behavioral / learning (L30) / long-duration suites.
