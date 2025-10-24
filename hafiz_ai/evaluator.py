"""Text-based recitation evaluation utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, Iterable, List, Optional

from .normalization import normalize_text, tokenize


@dataclass
class RecitationFeedback:
    """Structured feedback returned by :class:`RecitationEvaluator`."""

    accuracy_score: float
    matched_words: List[str] = field(default_factory=list)
    missing_words: List[str] = field(default_factory=list)
    extra_words: List[str] = field(default_factory=list)
    mispronounced_words: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class RecitationEvaluator:
    """Evaluate Qur'an recitations using text transcripts.

    The evaluator compares an expected transcript with the learner's transcript
    and optionally incorporates per-word pronunciation scores produced by an
    external speech model. A lightweight rule-based feedback engine generates
    actionable guidance for the learner.
    """

    def __init__(self, pronunciation_threshold: float = 0.85) -> None:
        self.pronunciation_threshold = pronunciation_threshold

    def evaluate(
        self,
        expected_text: str,
        actual_text: str,
        pronunciation_scores: Optional[Dict[str, float]] = None,
    ) -> RecitationFeedback:
        """Compare ``actual_text`` with ``expected_text`` and produce feedback."""

        normalized_expected = normalize_text(expected_text)
        normalized_actual = normalize_text(actual_text)

        expected_tokens = tokenize(normalized_expected)
        actual_tokens = tokenize(normalized_actual)

        accuracy, matched, missing, extra = self._compare_tokens(
            expected_tokens, actual_tokens
        )
        mispronounced = self._identify_mispronounced(
            matched, pronunciation_scores or {}
        )
        suggestions = self._build_suggestions(accuracy, missing, extra, mispronounced)

        return RecitationFeedback(
            accuracy_score=accuracy,
            matched_words=matched,
            missing_words=missing,
            extra_words=extra,
            mispronounced_words=mispronounced,
            suggestions=suggestions,
        )

    def _compare_tokens(
        self, expected_tokens: List[str], actual_tokens: List[str]
    ) -> (float, List[str], List[str], List[str]):
        matcher = SequenceMatcher(None, expected_tokens, actual_tokens)
        missing: List[str] = []
        extra: List[str] = []
        matched: List[str] = []

        total_expected = len(expected_tokens)
        matched_count = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                matched.extend(expected_tokens[i1:i2])
                matched_count += i2 - i1
            elif tag == "delete":
                missing.extend(expected_tokens[i1:i2])
            elif tag == "insert":
                extra.extend(actual_tokens[j1:j2])
            elif tag == "replace":
                missing.extend(expected_tokens[i1:i2])
                extra.extend(actual_tokens[j1:j2])

        accuracy = 100.0 if total_expected == 0 else (matched_count / total_expected) * 100
        return accuracy, matched, missing, extra

    def _identify_mispronounced(
        self, matched_tokens: Iterable[str], pronunciation_scores: Dict[str, float]
    ) -> List[str]:
        if not pronunciation_scores:
            return []

        normalized_scores = {
            normalize_text(word): score for word, score in pronunciation_scores.items()
        }
        mispronounced: List[str] = []

        for token in matched_tokens:
            normalized_token = normalize_text(token)
            if normalized_token not in normalized_scores:
                continue
            if normalized_scores[normalized_token] < self.pronunciation_threshold:
                mispronounced.append(token)

        return mispronounced

    def _build_suggestions(
        self,
        accuracy: float,
        missing: Iterable[str],
        extra: Iterable[str],
        mispronounced: Iterable[str],
    ) -> List[str]:
        suggestions: List[str] = []
        missing_list = list(missing)
        extra_list = list(extra)
        mispronounced_list = list(mispronounced)

        if missing_list:
            unique_missing = self._unique_ordered(missing_list)
            suggestions.append(
                "Eksik okunan kelimeleri tekrar gözden geçir: "
                + ", ".join(unique_missing)
            )
        if extra_list:
            unique_extra = self._unique_ordered(extra_list)
            suggestions.append(
                "Bu kelimeler metinde yer almıyor: " + ", ".join(unique_extra)
            )
        if mispronounced_list:
            unique_mispronounced = self._unique_ordered(mispronounced_list)
            suggestions.append(
                "Telaffuz çalışması önerilir: " + ", ".join(unique_mispronounced)
            )
        if accuracy >= 95.0 and not suggestions:
            suggestions.append("Harika! Okuman çok güçlü, bu tempoda devam et.")
        elif accuracy >= 80.0:
            suggestions.append(
                "Genel olarak iyi bir okuma. Küçük düzeltmelerle daha da güçlenecek."
            )
        else:
            suggestions.append(
                "Daha fazla tekrar ve rehber eşliğinde çalışma, akıcılığını artıracaktır."
            )

        return suggestions

    @staticmethod
    def _unique_ordered(tokens: Iterable[str]) -> List[str]:
        seen = set()
        ordered: List[str] = []
        for token in tokens:
            if token not in seen:
                ordered.append(token)
                seen.add(token)
        return ordered
