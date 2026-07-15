# Intent Taxonomy

**Status:** Normative (v0.16.0)  
**Module:** `acm.authority.taxonomy`

## Research basis

| Domain | Relevance |
|--------|-----------|
| Episodic / autobiographical memory (Tulving; Conway) | Experience, autobiography, history |
| Semantic memory | Concepts, associations, general memory |
| Self-schemas / identity | Assistant vs user identity |
| Goals & executive attention | Goals, projects, working memory |
| Metacognition & source monitoring | Reflection, learning, confidence, reconciliation |
| Question interpretation | Intent before generation |

## Implemented categories

### Cognitive (Memory Authority required)

| Intent | Owner (primary) |
|--------|-----------------|
| `assistant_identity` | Identity |
| `user_identity` | Identity (+ Remembering) |
| `identity` | Identity |
| `autobiography` | Remembering |
| `experience` | Remembering |
| `remembering` | Remembering |
| `long_term_memory` | Remembering |
| `working_memory` | Working memory |
| `current_context` | Context |
| `history` | Remembering |
| `decision_history` | Remembering |
| `project` | Remembering (+ Experiences, Concepts, Identity, Goals) |
| `pattern` | Remembering |
| `general_memory` | Remembering |
| `concept` | Concepts |
| `association` | Associations |
| `preference` | Remembering |
| `goal` | Goals |
| `reflection` | Reflection |
| `learning` | Learning |
| `confidence` | Confidence |
| `reconciliation` | Reconciliation |
| `uncertain` | Remembering (conservative) |

### Non-cognitive (host may execute; still classified by ACM)

| Intent | Notes |
|--------|-------|
| `procedural` | Write code/poem, install, refactor |
| `reasoning` | Pure puzzle / arithmetic |
| `planning` | Host planning without stored goal retrieval |
| `tool_request` | Run tools / commands |
| `general_knowledge` | World knowledge without self/shared cognitive ownership |
| `conversation_management` | Greetings, acknowledgements |
| `not_memory` | Residual non-cognitive |

## Deferred (documented, not implemented)

`simulation`, `prediction`, `analogy`, `creativity`, `emotion`,
`social_model`, `temporal_reasoning` — evidence-gated future work.

## Extensibility

New intents are additive StrEnum values with an ownership table entry. Hosts
must not invent parallel taxonomies that reassign cognitive ownership.
