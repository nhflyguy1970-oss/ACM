# Learning Research Foundations — ACM

**Status:** Canonical research foundation for L0 (design only)  
**Mode:** Architecture & evidence — **no Learning organ implementation**  
**Companions:** [`LEARNING_ARCHITECTURE.md`](LEARNING_ARCHITECTURE.md) · [`LEARNING_GOVERNANCE.md`](LEARNING_GOVERNANCE.md) · [`COGNITIVE_RESEARCH_FOUNDATIONS.md`](COGNITIVE_RESEARCH_FOUNDATIONS.md)

Evidence grades used throughout:

| Grade | Meaning |
|-------|---------|
| **Well-supported** | Broad empirical consensus across cognitive science / neuroscience textbooks and reviews |
| **Emerging** | Active research with converging but incomplete consensus |
| **Speculative** | Plausible hypotheses; must not be treated as established law |

---

## What is learning?

**Working definition for ACM (engineering):**  
*Learning is durable adaptation of cognitive structures driven by experience and evaluation, such that future encoding, remembering, and action-bias change in systematic, observable ways.*

Learning is not:

| Not learning | Why |
|--------------|-----|
| Remembering | Reconstructs present state; may lightly reconsolidate accessibility |
| Reflection | Evaluates & records judgment; does not adapt Structures |
| Knowledge import | External facts ≠ autobiographical / skill adaptation (Knowledge ≠ Memory) |
| Concept birth alone | Nucleation is meaning formation; Learning owns *adaptive policy of change* across repetitions and outcomes |
| Self-improvement of architecture | Policy / organ redesign is assent-gated governance |

### Scientific framing (well-supported)

- Learning involves **lasting change in the organism’s disposition to behave or represent** after experience (classical definitions in learning theory).  
- Multiple systems exist: **associative** (conditioning), **procedural / skill**, **episodic**, **semantic**, **reinforcement** (outcome-contingent), **error-driven** updates.  
- Humans do not have one “learn button”; systems interact (multi-memory theories — Squire, Baddeley, Tulving traditions — **well-supported**).

### Engineering translation

ACM Learning should be a **orchestrating organ** that applies *typed, auditable adaptations* to Concepts, Associations, Identity attributes, Goals, and accessibility parameters — never by rewriting Experience content.

---

## Distinctions (required clarity)

| Capability | Question | Changes durable structure? | Immutable history? |
|------------|----------|----------------------------|--------------------|
| Experience | What happened? | No (content frozen) | Is the history |
| Concept formation | What is this? | Yes (meaning nucleates) | Experiences stay; Concepts evolve |
| Association | How related? | Yes (links evolve) | Experiences stay |
| Remembering | What do I remember? | Accessibility light touch | Experiences stay |
| Reflection | What do I think about what I remember? | No (evaluates; births Reflective Experiences) | Adds Reflective Experiences |
| **Learning** | **What have I learned?** | **Yes — adaptation of living structures** | Experiences + Reflective lineage stay |

Concept formation already changes Concepts. Learning’s exclusive claim is: **outcome-sensitive, governed adaptation across organs** informed by Reflection and repetition—not the first formation of a nucleus.

---

## How humans appear to learn (functional summary)

### Well-supported patterns

1. **Repetition / practice** — increases strength and reduces error (power law of practice — well-supported).  
2. **Reinforcement & prediction error** — surprising outcomes drive larger updates (Rescorla–Wagner / TD-like accounts of learning signals — well-supported in behavioral literature; neural dopamine mapping is useful inspiration but ACM must not implement dopaminergic biology).  
3. **Error & correction** — feedback revises predictions and beliefs (well-supported).  
4. **Spacing & consolidation** — distributed practice and offline periods improve retention (spacing effect + sleep consolidation literature — well-supported behaviorally; sleep mechanisms still refined — emerging on exact mechanisms).  
5. **Transfer & generalization** — learning can extend beyond training instances via abstraction (well-supported as phenomenon; exact mechanisms emerging).  
6. **Interference & forgetting** — new learning can impede old; accessibility decays without deletion of all traces (well-supported).  
7. **Metacognitive monitoring** — judgments of learning and confidence affect study/strategy (well-supported in educational psychology).

### Emerging

- Precise binding of schema assimilation vs accommodation schedules.  
- Continuous vs discrete “insight” transitions.  
- Socially scaffolded learning dynamics for agents.

### Speculative (do not hard-code as ACM law)

- Exact cortical–hippocampal replay scripts as software architecture.  
- Claims that all intelligence reduces to one RL scalar.  
- Claims that language model weight training *is* human learning.

---

## What cognitive structures change?

| Structure | Typical human change | ACM target under Learning |
|-----------|----------------------|---------------------------|
| Episodic traces | Accrue; rarely “edited” | Experiences remain immutable |
| Semantic / concepts | Categorization, prototypes shift | Concept strength, prototypes, hierarchy proposals |
| Associations | Hebbian-like co-activation, causal links | Association strengths / kinds / dormancy |
| Skills / habits | Automaticity via practice | Future skill Concepts + procedure bias (later) |
| Preferences | Reinforced by affective outcomes | Preference attributes with lineage |
| Identity / self-schema | Privileged, slower, socially sensitive | Continuity-biased; high-impact assent |
| Goals | Priority & policy shift with outcomes | Goal importance / open–close dynamics |
| Confidence | Calibrated (or miscalibrated) by feedback | Confidence policy as Learning product |
| Accessibility | Cue routes strengthen/weaken | Forgetting as accessibility (future) |

### What should never occur automatically

- Destruction of Experience history.  
- Silent identity identity flips / schema erasure.  
- Silent merge of mature Concepts without proposal trail.  
- Self-rewriting of Learning policy / Activation Architecture constants.  
- Importing external “knowledge” as owned memory without adoption path.

---

## Influence factors (research → engineering)

| Factor | Evidence | ACM Learning implication |
|--------|----------|--------------------------|
| Successful experiences | Reinforcement strengthens | Boost Concept/Association on congruent Reflective `sufficient`/`consistency` |
| Mistakes / conflict | Error-driven learning | Use Reflective `contradiction`/`uncertainty` to contest or weaken, not delete history |
| Repetition | Practice law | Cumulative evidence_ids / strengthenings with diminishing returns |
| Novelty | Surprise elevates encoding | Novelty salience already at encode; Learning weights surprising Reflective outcomes more |
| Sleep / offline | Consolidation favors selective strengthening | Sleep organ applies *low-impact* Learning proposals; high-impact → assent |
| Forgetting | Accessibility ≠ erasure | Future Forgetting organ; Learning designs cool paths, not destruction |
| Uncertainty | Adaptive when honest | Preserve Reflective uncertainty; Learning may increase exploration bias later |
| Explanation | Improves retention when generative | Future: explanation-class templates as Learning evidence stubs — no CoT dumps |

---

## Competing theories (selected)

| Theory family | Claim | ACM stance |
|---------------|-------|------------|
| Multi-memory systems | Distinct systems interact | **Accepted** — maps to ACM organs |
| Pure associative network | Everything is links | **Partial** — Associations important; Concepts & Identity privileged |
| Pure RL agent | Single reward maximizes all | **Rejected as monopoly** — useful signals only |
| Biological neural simulation | Cognition = neuron fidelity | **Rejected** for ACM implementation |
| LLM fine-tune = learning | Weight updates are memory | **Rejected** as ACM Learning definition |
| Schema theory (Piaget-like) | Assimilation/accommodation | **Accepted as engineering metaphor** for Concept change |
| Predictive processing | Brain minimizes surprise | **Emerging** — informs Prediction organ later, not exclusive Learning |

---

## Accepted principles for ACM Learning

1. Learning adapts **living structures**, never Experience content.  
2. Learning is fed primarily by **Reflective Experiences** + reinforcement from encode/remember outcomes.  
3. Learning is **observable** and **lineaged**.  
4. Learning ≠ architectural self-modification.  
5. Automatic vs assent is defined in [`LEARNING_GOVERNANCE.md`](LEARNING_GOVERNANCE.md).  
6. Functional cognition: useful behavior change, not brain mimicry.

## Rejected ideas

- Silent overwrite of beliefs without lineage.  
- Neuron/synapse simulation as roadmap.  
- Treating RAG corpus growth as Learning.  
- Collapsing Reflection into Learning.  
- Unbounded identity plasticity.

---

## Open research questions remaining for M7 design review

- Exact numeric schedules for diminishing returns (assent if treated as policy constants).  
- When habit/automaticity graduates from Concept practice to a future Skill organ.  
- Cross-domain transfer algorithm (wait for Analogical foundations maturity).
