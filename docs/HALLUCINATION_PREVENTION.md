# Hallucination / Confabulation Prevention

**Status:** Normative + research note (v0.15.0)

## Cognitive science context (research)

Relevant constructs informing ACM’s correction:

| Construct | Implication for ACM |
|-----------|---------------------|
| Episodic reconstruction | Recall is constructive; ACM already reconstructs from Concepts/Experiences — **not** LLM completion |
| Source monitoring | Speakers must track origin of knowledge; ACM stamps provenance on encode and surfaces supporting ids |
| Confabulation | Filling gaps with plausible but ungrounded content — forbidden for hosts and blocked in soft attribute fallback |
| Metacognition / uncertainty | “I don’t know” is valid knowledge (known unknown) |
| False memory | Encoding generative speech as Experience is contamination — blocked by Memory Protection |
| Reality monitoring | Hypothetical/simulation products must never be spoken as autobiography |

## What ACM already had

- No LLM inside `acm/` cognition paths  
- `ExplanationClass.UNKNOWN` when activation empty  
- Immutable Experiences; reconciliation does not rewrite history  

## Gaps closed in v0.15.0 (required for this correction)

1. **Soft attribute confabulation** — recalling an unrelated first attribute / bare label as if it answered the cue.  
2. **Confidence boost on weak recall** — reconsolidation no longer reinforces unknown/low-confidence reconstructions.  
3. **Missing host gate** — `cognitive_respond` forces classify → ACM → structured result before speech.  
4. **Speech→memory path** — encode rejects LM/speech tags and forbidden external kinds.

## Documented future (not implemented here)

- Richer source-monitoring meta-attributes on every spoken claim  
- Explicit “told vs inferred vs reconstructed” tags in speech contracts  
- Host-side LM tool-forcing that refuses tokens outside ACM fields  

These are desirable metacognitive enhancements; not required to establish Memory Authority in v0.15.0.
