"""C5–C8 tests: evidence presentation, reflection explain, daily summary, adoption."""

from __future__ import annotations

from acm.api.engine import CognitiveEngine
from acm.authority.evidence_present import present_memory_evidence
from acm.provenance import ProvenanceSource, TRUSTED_USER_STATEMENT
from acm.reflection.explain import explain_reflection


def test_evidence_presentation_known() -> None:
    eng = CognitiveEngine(agent_id="ev")
    eng.encode("My favorite color is blue.", provenance=TRUSTED_USER_STATEMENT)
    view = eng.inspect_evidence("Show the evidence for my favorite color")
    assert "presentation" in view
    pres = view["presentation"]
    assert pres["schema"] == "acm.evidence_presentation.v1"
    assert pres["fabricated"] is False
    assert pres["redaction"] == "strict"
    assert present_memory_evidence(view, engine=eng)["fabricated"] is False


def test_evidence_presentation_unknown() -> None:
    eng = CognitiveEngine(agent_id="ev-u")
    view = eng.inspect_evidence("Show the evidence for my favorite unicorn flavor")
    assert view["presentation"]["status"] in {"unknown", "known"}
    assert view["presentation"]["fabricated"] is False


def test_reflection_explanation_structured() -> None:
    text = explain_reflection(
        {
            "outcomes": ["contradiction", "insight"],
            "contradictions": ["blue vs red"],
            "remembered_answer": "blue",
            "answer": "generic",
        }
    )
    assert "contradictory" in text.lower()
    assert "blue vs red" in text


def test_daily_learning_summary_read_only() -> None:
    eng = CognitiveEngine(agent_id="daily")
    eng.encode("I prefer tea.", provenance=TRUSTED_USER_STATEMENT)
    thought = eng.what_do_i_think("tea")
    eng.learn(reflective_experience_id=thought["reflective_experience_id"])
    before = eng.store_fingerprint()
    summary = eng.daily_learning_summary()
    assert summary["schema"] == "acm.daily_learning_summary.v1"
    assert summary["read_only"] is True
    assert summary["adaptation_count"] >= 0
    assert eng.store_fingerprint() == before
    slept = eng.sleep()
    assert "learning_summary" in slept


def test_adopt_knowledge_mvp() -> None:
    eng = CognitiveEngine(agent_id="adopt")
    exp_before = len(eng.store.experiences)
    result = eng.adopt_knowledge(
        "Rust ownership rules prevent data races.",
        source_label="Rust Book",
    )
    assert result["adopted"] is True
    assert result["autobiographical"] is False
    assert len(eng.store.experiences) == exp_before + 1
    eid = result["experience_id"]
    exp = eng.store.experiences[eid]
    assert exp.meta_dict().get("adopted_knowledge") == "1"
    assert any(
        p.origin == ProvenanceSource.ADOPTED_KNOWLEDGE
        for p in eng.store.provenance.values()
        if p.artifact_id == eid
    )


def test_adopt_knowledge_rejects_bulk_and_identity_without_assent() -> None:
    eng = CognitiveEngine(agent_id="adopt-gate")
    bulk = "line\n" * 50 + ("x" * 100)
    assert eng.adopt_knowledge(bulk, source_label="dump")["reason"] == "bulk_rejected"
    denied = eng.adopt_knowledge(
        "My name is AdoptedName.",
        source_label="doc",
        kind="identity",
        assent=False,
    )
    assert denied["adopted"] is False
    assert denied["reason"] == "assent_required"


def test_adopt_then_learn_does_not_invent_extra_experiences_from_learning() -> None:
    eng = CognitiveEngine(agent_id="adopt-learn")
    eng.adopt_knowledge("HTTP is a request-response protocol.", source_label="RFC")
    before = len(eng.store.experiences)
    thought = eng.what_do_i_think("HTTP protocol")
    # Reflection may birth a Reflective Experience — Learning must not invent more
    mid = len(eng.store.experiences)
    eng.learn(reflective_experience_id=thought["reflective_experience_id"])
    after = len(eng.store.experiences)
    assert after == mid  # learning reorganizes only
    assert mid >= before  # reflection may add reflective exp
