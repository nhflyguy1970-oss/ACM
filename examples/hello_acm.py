#!/usr/bin/env python3
"""Minimal ACM integration example — no host framework required."""

from __future__ import annotations

from acm import CognitiveEngine


def main() -> None:
    engine = CognitiveEngine(agent_id="demo-agent")
    engine.open_goal("Learn user preferences", importance=0.7)
    engine.encode("I am a portable cognitive memory engine.", kind="identity")
    engine.encode("My favorite coffee is dark roast.", kind="preference")
    print(engine.who_am_i()["answer"])
    print("what_happened:", [e["cognitive_kind"] for e in engine.what_happened()])
    print("what_is_this:", engine.what_is_this("coffee")["answer"])
    result = engine.remember("What is my favorite coffee?")
    print(result.answer)
    print(result.explanation)
    print("confidence:", round(result.confidence, 3))
    sketch = engine.metacognitive_sketch()
    print("know_count:", sketch["what_i_know_count"])
    print("identity:", sketch["identity"])
    print("experience:", sketch["experience"])
    print("concept:", sketch["concept"])
    snap = engine.validation.snapshot()
    print("activations:", snap["counts"]["activations"])
    print("identity_metrics:", snap["identity"])
    print("experience_metrics:", snap["experience"])
    print("concept_metrics:", snap["concept"])
    sleep = engine.sleep()
    print("sleep:", sleep)


if __name__ == "__main__":
    main()
