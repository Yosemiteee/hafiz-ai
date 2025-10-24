"""Tests for the RecitationEvaluator."""

from hafiz_ai.evaluator import RecitationEvaluator


def test_detects_missing_word():
    evaluator = RecitationEvaluator()
    feedback = evaluator.evaluate(
        expected_text="بسم الله الرحمن الرحيم",
        actual_text="بسم الله الرحيم",
    )

    assert feedback.accuracy_score < 100
    assert feedback.missing_words == ["الرحمن"]
    assert feedback.extra_words == []


def test_pronunciation_feedback_uses_threshold():
    evaluator = RecitationEvaluator(pronunciation_threshold=0.9)
    feedback = evaluator.evaluate(
        expected_text="الحمد لله رب العالمين",
        actual_text="الحمد لله رب العالمين",
        pronunciation_scores={"العالمين": 0.85, "الحمد": 0.95},
    )

    assert feedback.mispronounced_words == ["العالمين"]
    assert any("Telaffuz" in suggestion for suggestion in feedback.suggestions)


def test_extra_words_are_listed():
    evaluator = RecitationEvaluator()
    feedback = evaluator.evaluate(
        expected_text="إياك نعبد وإياك نستعين",
        actual_text="إياك وحدك نعبد وإياك نستعين",
    )

    assert feedback.extra_words == ["وحدك"]
    assert any("Bu kelimeler" in suggestion for suggestion in feedback.suggestions)
