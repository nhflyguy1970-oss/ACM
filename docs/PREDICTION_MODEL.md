# Prediction Model — ACM

**Status:** Canonical for M11 (implemented)  
**Cognitive question:** *Based upon memory, what is likely?*  
**Companions:** [`PREDICTIVE_MEMORY.md`](PREDICTIVE_MEMORY.md) · [`MENTAL_SIMULATION.md`](MENTAL_SIMULATION.md) · [`BIOLOGICAL_VS_TECHNICAL_FUNCTION.md`](BIOLOGICAL_VS_TECHNICAL_FUNCTION.md)

## Biological function

Prospective memory and predictive processing help organisms anticipate upcoming cues and outcomes from prior experience (**well-supported** behaviorally; mechanistic neural accounts vary — **emerging**). Prediction reduces surprise costs during encoding and retrieval.

## Technical function

Prediction estimates **probable future memory outcomes** from living cognitive structures via the singular Activation Architecture. It never chooses actions, plans sequences of goals, or makes decisions.

| Field | Content |
|-------|---------|
| Organ | `PredictionOrgan` |
| Inputs | Cue + Activation field + Associations + Priority + Accessibility + Learning residue |
| Outputs | Predicted outcomes with probabilistic confidences; Prediction Artifacts |
| Validation | Outcomes are distributional; history unchanged; no plan verbs |

## Ownership

| Owns | Does not own |
|------|----------------|
| Likelihood / expectation / anticipation over memory | Planning, decision making, action selection |
| Prediction confidence evolution + audit trail | Creating Experiences |
| Competing hypotheses lifecycle (counterfactual claims) | Reasoning chains / CoT |
| Prediction accuracy observables | Deleting provenance |

## Intentional omissions

Neuron-level predictive coding, forward models of actuators, policy search, deterministic oracles.

## Cap deepening

- Cap3: hypotheses + prediction audits — [`PREDICTION_AUDIT.md`](PREDICTION_AUDIT.md)
- Cap4: multi-level abstractions — [`MULTI_LEVEL_ABSTRACTION.md`](MULTI_LEVEL_ABSTRACTION.md)
