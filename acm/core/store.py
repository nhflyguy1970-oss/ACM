"""In-memory cognitive substrate — informative technology choice, swappable later."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any

from acm.concepts.model import Concept, ConceptStage
from acm.experiences.model import Experience
from acm.types import ConceptRole, EdgeType, EnvelopeRef, new_id


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
    """Minimal durable-feeling store kept in process for foundational milestones."""

    def __init__(self) -> None:
        self.experiences: dict[str, Experience] = {}
        self.concepts: dict[str, Concept] = {}
        self.associations: dict[str, Association] = {}
        self.goals: dict[str, Goal] = {}
        self.envelopes: dict[str, EnvelopeRef] = {}

    def add_concept(
        self, label: str, role: ConceptRole = ConceptRole.ENTITY, **kwargs: Any
    ) -> Concept:
        now = time()
        stage = kwargs.pop("stage", ConceptStage.NUCLEUS)
        concept = Concept(
            id=new_id("con"),
            labels=[label],
            role=role,
            first_seen=now,
            last_activated=now,
            stage=stage,
            **kwargs,
        )
        self.concepts[concept.id] = concept
        return concept

    def find_concepts_by_label(self, text: str) -> list[Concept]:
        q = text.lower()
        hits: list[Concept] = []
        for c in self.concepts.values():
            if c.stage == ConceptStage.RETIRED:
                continue
            if not c.active and c.stage != ConceptStage.DORMANT:
                continue
            for lab in c.labels:
                lab_l = lab.lower()
                if lab_l == q or (len(q) >= 4 and (q in lab_l.split() or lab_l in q.split())):
                    hits.append(c)
                    break
            else:
                for attr in c.attributes:
                    if attr.active and (
                        attr.value.lower() == q
                        or (len(q) >= 4 and q in attr.value.lower())
                        or q in attr.key.lower()
                    ):
                        hits.append(c)
                        break
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
            if other and (other.active or other.stage == ConceptStage.DORMANT):
                out.append((edge, other))
        out.sort(key=lambda x: x[0].weight, reverse=True)
        return out

    def add_goal(self, title: str, **kwargs: Any) -> Goal:
        goal = Goal(id=new_id("goal"), title=title, created=time(), **kwargs)
        self.goals[goal.id] = goal
        return goal

    def active_goals(self) -> list[Goal]:
        return [g for g in self.goals.values() if g.status == "active"]
