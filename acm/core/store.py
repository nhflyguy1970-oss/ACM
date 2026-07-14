"""In-memory cognitive substrate — informative technology choice, swappable later."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any

from acm.types import Attribute, ConceptRole, EdgeType, EnvelopeRef, new_id


@dataclass
class Experience:
    id: str
    summary: str
    timestamp: float
    context_tags: tuple[str, ...] = ()
    goal_ids: list[str] = field(default_factory=list)
    envelope_ids: list[str] = field(default_factory=list)
    attention_class: str = "default"
    importance: float = 0.5
    version: int = 1
    active: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Concept:
    id: str
    labels: list[str]
    role: ConceptRole = ConceptRole.ENTITY
    attributes: list[Attribute] = field(default_factory=list)
    envelope_ids: list[str] = field(default_factory=list)
    strength: float = 0.5
    importance: float = 0.5
    confidence: float = 0.6
    access_count: int = 0
    first_seen: float = 0.0
    last_activated: float = 0.0
    provisional: bool = True
    active: bool = True
    identity: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Association:
    id: str
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float = 0.5
    active: bool = True


@dataclass
class Goal:
    id: str
    title: str
    status: str = "active"  # active | completed | abandoned | superseded
    importance: float = 0.6
    created: float = 0.0
    completed: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class CognitiveStore:
    """Minimal durable-feeling store kept in process for M0–M3 foundations."""

    def __init__(self) -> None:
        self.experiences: dict[str, Experience] = {}
        self.concepts: dict[str, Concept] = {}
        self.associations: dict[str, Association] = {}
        self.goals: dict[str, Goal] = {}
        self.envelopes: dict[str, EnvelopeRef] = {}

    def add_experience(self, summary: str, **kwargs: Any) -> Experience:
        exp = Experience(
            id=new_id("exp"),
            summary=summary,
            timestamp=time(),
            **kwargs,
        )
        self.experiences[exp.id] = exp
        return exp

    def add_concept(
        self, label: str, role: ConceptRole = ConceptRole.ENTITY, **kwargs: Any
    ) -> Concept:
        now = time()
        concept = Concept(
            id=new_id("con"),
            labels=[label],
            role=role,
            first_seen=now,
            last_activated=now,
            **kwargs,
        )
        self.concepts[concept.id] = concept
        return concept

    def find_concepts_by_label(self, text: str) -> list[Concept]:
        q = text.lower()
        hits: list[Concept] = []
        for c in self.concepts.values():
            if not c.active:
                continue
            if any(q in lab.lower() or lab.lower() in q for lab in c.labels):
                hits.append(c)
            for attr in c.attributes:
                if attr.active and (q in attr.value.lower() or q in attr.key.lower()):
                    hits.append(c)
                    break
        # unique preserve order
        seen: set[str] = set()
        out: list[Concept] = []
        for h in hits:
            if h.id not in seen:
                seen.add(h.id)
                out.append(h)
        return out

    def add_association(
        self,
        source_id: str,
        target_id: str,
        edge_type: EdgeType = EdgeType.RELATED_TO,
        weight: float = 0.5,
    ) -> Association:
        edge = Association(
            id=new_id("edge"),
            source_id=source_id,
            target_id=target_id,
            edge_type=edge_type,
            weight=weight,
        )
        self.associations[edge.id] = edge
        return edge

    def neighbors(self, concept_id: str) -> list[tuple[Association, Concept]]:
        out: list[tuple[Association, Concept]] = []
        for edge in self.associations.values():
            if not edge.active:
                continue
            other = None
            if edge.source_id == concept_id:
                other = self.concepts.get(edge.target_id)
            elif edge.target_id == concept_id:
                other = self.concepts.get(edge.source_id)
            if other and other.active:
                out.append((edge, other))
        out.sort(key=lambda x: x[0].weight, reverse=True)
        return out

    def add_goal(self, title: str, **kwargs: Any) -> Goal:
        goal = Goal(id=new_id("goal"), title=title, created=time(), **kwargs)
        self.goals[goal.id] = goal
        return goal

    def active_goals(self) -> list[Goal]:
        return [g for g in self.goals.values() if g.status == "active"]
