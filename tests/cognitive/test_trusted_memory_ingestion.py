"""D046 — Trusted Memory Ingestion trust-boundary certification."""

from __future__ import annotations

from pathlib import Path

import pytest

from acm import CognitiveEngine, __version__
from acm.provenance import (
    TRUSTED_USER_CORRECTION,
    TRUSTED_USER_STATEMENT,
    TRUSTED_USER_TEACHING,
    HostOperation,
    IngestionActor,
    IngestionProvenance,
    MessageRole,
)


def _counts(engine: CognitiveEngine) -> tuple[int, int, int]:
    return (
        len(engine.store.experiences),
        len(engine.store.concepts),
        len(engine.store.provenance),
    )


def _source(
    actor: IngestionActor,
    operation: HostOperation,
    role: MessageRole,
) -> IngestionProvenance:
    return IngestionProvenance(
        actor=actor,
        host_operation=operation,
        message_role=role,
    )


UNTRUSTED_CASES = (
    (
        "Tool memory_search worked for: Show the evidence for my favorite color.",
        _source(IngestionActor.TOOL, HostOperation.MEMORY_SEARCH, MessageRole.TOOL_RESULT),
    ),
    (
        "Tool execution output: My favorite color is command-cyan.",
        _source(IngestionActor.TOOL, HostOperation.TOOL_EXECUTION, MessageRole.TOOL_RESULT),
    ),
    (
        "memory_search result: My favorite color is internal-blue.",
        _source(IngestionActor.MEMORY, HostOperation.RETRIEVAL, MessageRole.TOOL_RESULT),
    ),
    (
        "Reflection trace: My favorite color is inferred-green.",
        _source(
            IngestionActor.REFLECTION,
            HostOperation.REFLECTION,
            MessageRole.REFLECTION_OUTPUT,
        ),
    ),
    (
        "Diagnostic: My favorite color is probe-yellow.",
        _source(
            IngestionActor.DIAGNOSTIC,
            HostOperation.DIAGNOSTIC,
            MessageRole.DIAGNOSTIC_OUTPUT,
        ),
    ),
    (
        "Prompt fragment: My favorite color is prompt-purple.",
        _source(IngestionActor.SYSTEM, HostOperation.SYSTEM_EVENT, MessageRole.PROMPT_TEXT),
    ),
    (
        "System message: My favorite color is system-orange.",
        _source(IngestionActor.SYSTEM, HostOperation.SYSTEM_EVENT, MessageRole.SYSTEM_MESSAGE),
    ),
    (
        "Implementation metadata: My favorite color is metadata-black.",
        _source(IngestionActor.INFRASTRUCTURE, HostOperation.ENCODING, MessageRole.METADATA),
    ),
    (
        "Infrastructure log: My favorite color is log-white.",
        _source(
            IngestionActor.INFRASTRUCTURE,
            HostOperation.SYSTEM_EVENT,
            MessageRole.INFRASTRUCTURE_LOG,
        ),
    ),
    (
        "Assistant reply: My favorite color is assistant-silver.",
        _source(
            IngestionActor.ASSISTANT,
            HostOperation.CONVERSATION,
            MessageRole.ASSISTANT_REPLY,
        ),
    ),
    (
        "Mislabeled retrieval text: My favorite color is retrieved-pink.",
        _source(
            IngestionActor.USER,
            HostOperation.RETRIEVAL,
            MessageRole.USER_STATEMENT,
        ),
    ),
    (
        "Mislabeled tool role: My favorite color is role-brown.",
        _source(
            IngestionActor.USER,
            HostOperation.ENCODING,
            MessageRole.TOOL_RESULT,
        ),
    ),
)


def test_d046_version_pin() -> None:
    assert tuple(int(p) for p in __version__.split(".")) >= (0, 19, 0)


def test_d046_missing_and_unknown_provenance_rejected_before_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = CognitiveEngine(agent_id="d046")
    before = _counts(engine)
    before_context = engine.context

    def _must_not_extract(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("semantic extraction must not run")

    monkeypatch.setattr("acm.semantic.extract_semantics", _must_not_extract)
    missing = engine.encode("My favorite color is blue.")
    unknown = engine.encode(
        "My favorite color is blue.",
        provenance=_source(
            IngestionActor.UNKNOWN,
            HostOperation.UNKNOWN,
            MessageRole.UNKNOWN,
        ),
    )
    unknown_operation = engine.encode(
        "My favorite color is blue.",
        provenance=_source(
            IngestionActor.USER,
            HostOperation.UNKNOWN,
            MessageRole.USER_STATEMENT,
        ),
    )
    unknown_role = engine.encode(
        "My favorite color is blue.",
        provenance=_source(
            IngestionActor.USER,
            HostOperation.ENCODING,
            MessageRole.UNKNOWN,
        ),
    )

    assert missing["encoded"] is False
    assert missing["reason"] == "memory_trust"
    assert missing["detail"] == "missing_provenance"
    assert unknown["encoded"] is False
    assert unknown["detail"] == "unknown_actor"
    assert unknown_operation["detail"] == "unknown_host_operation"
    assert unknown_role["detail"] == "unknown_message_role"
    assert _counts(engine) == before
    assert engine.context is before_context


@pytest.mark.parametrize(("text", "provenance"), UNTRUSTED_CASES)
def test_d046_non_user_sources_never_create_autobiographical_memory(
    text: str,
    provenance: IngestionProvenance,
) -> None:
    engine = CognitiveEngine(agent_id="d046")
    before = _counts(engine)
    result = engine.encode(text, kind="preference", pin=True, provenance=provenance)

    assert result["encoded"] is False
    assert result["reason"] == "memory_trust"
    assert result["ingestion"]["eligible"] is False
    assert _counts(engine) == before
    recall = engine.cognitive_respond("What is my favorite color?")
    assert recall["status"] == "unknown"
    assert recall["memory"] is None


def test_d046_tool_artifact_cannot_displace_valid_preference() -> None:
    engine = CognitiveEngine(agent_id="d046")
    valid = engine.encode(
        "My favorite color is blue.",
        kind="preference",
        provenance=TRUSTED_USER_TEACHING,
    )
    assert valid["encoded"] is True

    artifact = UNTRUSTED_CASES[0]
    for _ in range(10):
        rejected = engine.encode(artifact[0], provenance=artifact[1])
        assert rejected["encoded"] is False

    result = engine.cognitive_respond("What is my favorite color?")
    assert result["status"] == "known"
    assert result["memory"] == "Your favorite color is blue."
    assert result["uncertainty"] is None


@pytest.mark.parametrize(
    ("text", "provenance"),
    (
        ("My favorite color is blue.", TRUSTED_USER_TEACHING),
        ("My name is Jeff.", TRUSTED_USER_STATEMENT),
        ("My dog's name is Max.", TRUSTED_USER_STATEMENT),
        ("I prefer local models.", TRUSTED_USER_STATEMENT),
        ("Actually, my favorite color is red.", TRUSTED_USER_CORRECTION),
    ),
)
def test_d046_genuine_user_knowledge_still_encodes(
    text: str,
    provenance: IngestionProvenance,
) -> None:
    engine = CognitiveEngine(agent_id="d046")
    result = engine.encode(text, provenance=provenance)

    assert result["encoded"] is True
    assert result["ingestion"]["eligible"] is True
    assert result["ingestion"]["reason"].startswith("trusted_user_")
    experience = engine.store.experiences[result["experience_id"]]
    assert dict(experience.metadata)["source_actor"] == "user"


def test_d046_source_metadata_is_durable_and_auditable(tmp_path: Path) -> None:
    path = tmp_path / "trusted.db"
    engine = CognitiveEngine(agent_id="d046", persist_path=str(path), auto_persist=True)
    encoded = engine.encode(
        "My favorite color is blue.",
        kind="preference",
        provenance=TRUSTED_USER_TEACHING,
    )
    exp_id = encoded["experience_id"]
    concept_id = encoded["concept_id"]

    for artifact_id in (exp_id, concept_id):
        records = engine.provenance_of(artifact_id)
        assert records
        assert records[0]["source_actor"] == "user"
        assert records[0]["host_operation"] == "encoding"
        assert records[0]["message_role"] == "user_teaching"
        assert records[0]["eligibility_reason"] == "trusted_user_teaching"

    restarted = CognitiveEngine(agent_id="d046", persist_path=str(path), auto_persist=True)
    persisted = restarted.provenance_of(exp_id)
    assert persisted
    assert persisted[0]["source_actor"] == "user"
    assert persisted[0]["host_operation"] == "encoding"
    assert persisted[0]["message_role"] == "user_teaching"
    metadata = dict(restarted.store.experiences[exp_id].metadata)
    assert metadata["source_eligibility_reason"] == "trusted_user_teaching"
    assert restarted.cognitive_respond("What is my favorite color?")["memory"] == (
        "Your favorite color is blue."
    )


def test_d046_assistant_operational_identity_uses_configuration_not_encode() -> None:
    engine = CognitiveEngine(
        agent_id="aria",
        assistant_identity={"name": "Aria", "role": "memory assistant"},
    )
    rejected = engine.encode(
        "I am a research assistant.",
        kind="identity",
        speaker="assistant",
        provenance=_source(
            IngestionActor.ASSISTANT,
            HostOperation.ENCODING,
            MessageRole.ASSISTANT_REPLY,
        ),
    )
    assert rejected["encoded"] is False
    result = engine.cognitive_respond("Who are you?")
    assert result["status"] == "known"
    assert "aria" in (result["memory"] or "").lower()
