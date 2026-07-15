# Certification Framework — ACM

**Status:** Canonical for Phase 2 (P2.5)  
**Critical:** Builds the framework. **Does not certify.**

## Checklist gates

Persistence roundtrip · checksum integrity · backup/restore · provenance stamps · shadow legacy-authoritative · adapter capabilities · encode p95 · long-duration smoke · (documented checklist includes migration/rollback/daily-use placeholders)

## API

```python
from acm.certification import CertificationFramework
report = CertificationFramework(workdir="./cert_out").run_all()
assert report["certified"] is False
```

## Report

`acm.certification/0.13` JSON with gate results. `certified` is **always false** until a future explicit certification phase.
