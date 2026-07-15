# Cognitive Dispatch Validation

**Status:** Normative (v0.17.0)  
**Suite:** `tests/cognitive/test_cognitive_dispatch.py`  
**Regression:** intent routing + Memory Authority suites

## Coverage

- Identity routing (assistant / user; no assistant bleed on “Who am I?”)
- Goal / project / reflection / learning / association / remembering terminals
- Unknown & multi-organ reconstruction
- Infrastructure leakage / forbidden terminals
- Raw storage / adaptation dump rejection
- Diagnostics completeness
- Host independence
- Performance batch bound
- Memory Authority preservation

## Run

```bash
pytest tests/cognitive/test_cognitive_dispatch.py tests/cognitive/test_cognitive_intent_routing.py tests/cognitive/test_memory_authority.py -q
```
