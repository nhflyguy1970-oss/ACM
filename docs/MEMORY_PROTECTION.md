# Memory Protection

**Status:** Normative (v0.15.0)

## Rule

Language-model output SHALL NEVER become cognitive memory.

Generated responses are **not**:

- Experiences  
- Learning  
- Reflections  
- Concepts  
- Associations  
- Evidence  

Memory is created only through legitimate ACM processes (`encode`, revise,
assent-gated identity, Learning adaptations, Offline proposals with governance).

## Encode gate

`reject_speech_contamination` blocks encode when:

- context tags include `llm_generated`, `speech_output`, `assistant_utterance`, …  
- `external_kind` is `llm` / `speech` / `generated` / …  
- provenance origin matches forbidden markers  
- text self-identifies fabrication  

See `MEMORY_PROTECTION_TAGS` in `acm.authority.protection`.

## Host checklist

- [ ] Do not pass chat completions into `encode`  
- [ ] Tag any speculative host text so ACM rejects it if mis-routed  
- [ ] Persist only ACM-approved Experiences to durable store
