# Unknown Memory

**Status:** Normative (v0.15.0)

## Thesis

Unknown is knowledge. Low confidence is knowledge. Insufficient evidence is knowledge.

ACM must return these as **first-class statuses**, not as invitations for a
language model to invent content.

## Status mapping

| Status | Meaning | Speech duty |
|--------|---------|-------------|
| `unknown` | No reliable reconstruction | “I don’t currently know.” |
| `insufficient_evidence` | Activation without cue grounding | “I don’t yet have enough experiences.” |
| `low_confidence` | Below authority threshold | “I am not confident enough to answer.” |
| `conflicting` | Competing recollections | Disclose conflict; do not silently pick |
| `known` | Grounded reconstruction | Speak ACM `memory` field only |

## Implementation

- Gates: `acm.authority.gates`  
- Speech: `acm.authority.speak`  
- Pipeline strips propositional `memory` for unknown / insufficient / low_confidence

Hosts that paraphrase must preserve the status — never promote unknown to known.
