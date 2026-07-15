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
    engine.encode("A husky is a dog.", pin=True)
    print("how_related:", engine.how_related("husky", "dog")["answer"])
    remembered = engine.what_do_i_remember("What is my favorite coffee?")
    print("what_do_i_remember:", remembered["answer"], "ambiguous=", remembered.get("ambiguous"))
    thought = engine.what_do_i_think("What is my favorite coffee?")
    print("what_do_i_think:", thought["answer"])
    print("outcomes:", thought["outcomes"])
    result = engine.remember("What is my favorite coffee?")
    print(result.answer)
    print(result.explanation)
    print("confidence:", round(result.confidence, 3))
    sketch = engine.metacognitive_sketch()
    print("know_count:", sketch["what_i_know_count"])
    print("identity:", sketch["identity"])
    print("experience:", sketch["experience"])
    print("concept:", sketch["concept"])
    print("association:", sketch.get("association"))
    print("remembering:", sketch.get("remembering"))
    print("reflection:", sketch.get("reflection"))
    snap = engine.validation.snapshot()
    print("activations:", snap["counts"]["activations"])
    print("identity_metrics:", snap["identity"])
    print("experience_metrics:", snap["experience"])
    print("concept_metrics:", snap["concept"])
    print("association_metrics:", snap["association"])
    print("remembering_metrics:", snap["remembering"])
    print("reflection_metrics:", snap["reflection"])
    sleep = engine.sleep()
    print("sleep:", sleep)


if __name__ == "__main__":
    main()
