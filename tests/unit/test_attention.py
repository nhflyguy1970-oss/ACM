from __future__ import annotations

from acm.attention.field import classify_attention, encode_weight
from acm.types import AttentionClass


def test_pin_and_preference_classes() -> None:
    assert classify_attention("Please remember this fact") == AttentionClass.USER_PIN
    assert classify_attention("My favorite tea is green") == AttentionClass.NOVELTY
    assert classify_attention("Actually change that") == AttentionClass.PREDICTION_ERROR
    assert classify_attention("hello world") == AttentionClass.DEFAULT


def test_encode_weights_ordered() -> None:
    assert encode_weight(AttentionClass.USER_PIN) > encode_weight(AttentionClass.DEFAULT)
    assert encode_weight(AttentionClass.NOVELTY) >= 0.5
