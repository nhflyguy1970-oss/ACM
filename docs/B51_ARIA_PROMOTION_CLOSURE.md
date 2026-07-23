# B51 — Aria Identity/Preference Promotion Closure

**Status:** COMPLETE — ACM v0.44.0 / Aria `aria-acm-v0.43.0-1`+  
**Date:** 2026-07-23

## Decision

B51 is **complete**. The Intent (promote certified D038–D045 Identity/Preference
stack into Aria’s vendored ACM) is already satisfied by the continuous promotion
program.

## Evidence

Aria `aria_acm/VERSION.json` `includes` lists:

`D038` … `D047`, plus M4/M5 caps and B09–B13, B20, B21, B36, B47.

Vendored ACM tracks standalone ACM commit pins with tree hash certification.
Host suites `tests/test_aria_acm_*.py` enforce pin + behavioral parity after
each promotion.

## Why this closes B51

B51’s problem statement (“Aria remains on older cognition until promotion”) is
obsolete: Aria’s nested `aria_acm/` copy is synchronized after every certified
practical backlog item in this completion program.

No additional one-shot Identity/Preference promotion is required.

## Related

- Aria `aria_acm/VERSION.json`
- `docs/ARIA_INTEGRATION_ARCHITECTURE.md`
- Backlog B51
