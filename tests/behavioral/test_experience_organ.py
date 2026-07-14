from __future__ import annotations

from acm import CognitiveEngine
from acm.experiences import CognitiveKind, ExperienceLifecycle


def test_what_happened_answers_chronology() -> None:
    engine = CognitiveEngine(agent_id="exp")
    engine.open_goal("Ship M2")
    engine.encode("I discovered a chronology bug.", pin=True)
    engine.encode("I decided to fix the ordering.", pin=True)
    events = engine.what_happened()
    assert len(events) >= 2
    assert events[0]["sequence"] < events[1]["sequence"]
    assert events[-1]["cognitive_kind"] in {
        CognitiveKind.DECISION.value,
        CognitiveKind.DISCOVERY.value,
        CognitiveKind.OBSERVATION.value,
    }
    tl = engine.timeline()
    assert tl["question"] == "What happened?"
    assert tl["count"] >= 2


def test_immutability_and_lineage_on_revise() -> None:
    engine = CognitiveEngine(agent_id="exp")
    first = engine.encode("The build failed unexpectedly.", pin=True)
    eid = first["experience_id"]
    original = engine.store.experiences[eid]
    revised = engine.revise_experience(eid, "Actually, the build succeeded after retry.")
    assert revised["encoded"] is True
    # Prior content unchanged
    still = engine.store.experiences[eid]
    assert still.summary == original.summary
    assert still.cognitive_kind == original.cognitive_kind
    assert revised["experience"]["revises_id"] == eid
    assert engine.experiences.lifecycle_of(eid) == ExperienceLifecycle.DORMANT
    chain = engine.experiences.lineage_chain(revised["experience_id"])
    assert eid in chain
    assert revised["experience_id"] in chain


def test_multimodal_envelope_equal_status() -> None:
    engine = CognitiveEngine(agent_id="exp")
    env_img = engine.experiences.attach_envelope(
        content_hash="sha256:img1", kind="image", mime="image/png"
    )
    env_code = engine.experiences.attach_envelope(
        content_hash="sha256:code1", kind="code", mime="text/x-python"
    )
    a = engine.encode(
        "I saw an architecture diagram.",
        pin=True,
        external_kind="image",
        envelope_ids=(env_img,),
    )
    b = engine.encode(
        "I learned from the code sample.",
        pin=True,
        external_kind="code",
        envelope_ids=(env_code,),
    )
    assert a["experience"]["external_kind"] == "image"
    assert b["experience"]["external_kind"] == "code"
    assert a["experience"]["envelope_ids"] == [env_img]
    assert b["experience"]["envelope_ids"] == [env_code]


def test_identity_and_goal_influence_on_experience() -> None:
    engine = CognitiveEngine(agent_id="exp")
    engine.open_goal("Become reliable")
    out = engine.encode("I am a portable memory engine.", kind="identity")
    assert out["experience"]["cognitive_kind"] == CognitiveKind.IDENTITY_CHANGE.value
    assert out["experience"]["identity_influenced"] is True
    assert out["experience"]["goal_ids"]
    assert out["experience"]["salience_birth"]["goal_relevance"] > 0


def test_goal_completion_births_experience() -> None:
    engine = CognitiveEngine(agent_id="exp")
    gid = engine.open_goal("Finish Experience organ")
    engine.complete_goal(gid)
    kinds = [e["cognitive_kind"] for e in engine.what_happened(include_dormant=True)]
    assert CognitiveKind.GOAL_COMPLETION.value in kinds
