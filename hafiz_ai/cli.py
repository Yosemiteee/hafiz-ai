"""Command-line interface for Hafız AI recitation evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional

from .evaluator import RecitationEvaluator
from .normalization import normalize_text


def _read_text_argument(value: Optional[str], file_path: Optional[Path]) -> str:
    if value and file_path:
        raise ValueError("Metin ve dosya argümanları aynı anda kullanılamaz.")
    if value:
        return value
    if file_path:
        return file_path.read_text(encoding="utf-8")
    raise ValueError("Metin veya dosya argümanlarından biri sağlanmalıdır.")


def _parse_pronunciation_scores(values: Optional[List[str]]) -> Dict[str, float]:
    if not values:
        return {}
    scores: Dict[str, float] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(
                "Telaffuz skorları 'kelime=0.9' formatında belirtilmelidir."
            )
        word, score_str = item.split("=", 1)
        try:
            scores[normalize_text(word)] = float(score_str)
        except ValueError as exc:  # pragma: no cover - defensive programming
            raise ValueError(f"Geçersiz skor değeri: {item}") from exc
    return scores


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Hafızların Kur'an ezberini takip etmeye yardımcı olan metin tabanlı "
            "bir değerlendirme aracı."
        )
    )
    expected_group = parser.add_mutually_exclusive_group(required=True)
    expected_group.add_argument("--expected", help="Beklenen (referans) metin")
    expected_group.add_argument(
        "--expected-file", type=Path, help="Beklenen metni içeren dosya"
    )

    transcript_group = parser.add_mutually_exclusive_group(required=True)
    transcript_group.add_argument("--transcript", help="Öğrencinin okuma metni")
    transcript_group.add_argument(
        "--transcript-file", type=Path, help="Öğrenci okumasını içeren dosya"
    )

    parser.add_argument(
        "--pronunciation-score",
        action="append",
        dest="pronunciation_scores",
        help="Telaffuz skorlarını 'kelime=0.92' formatında ekleyin",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.85,
        help="Telaffuz değerlendirmesi için eşik değeri (varsayılan: 0.85)",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    expected_text = _read_text_argument(args.expected, args.expected_file)
    transcript_text = _read_text_argument(args.transcript, args.transcript_file)
    pronunciation_scores = _parse_pronunciation_scores(args.pronunciation_scores)

    evaluator = RecitationEvaluator(pronunciation_threshold=args.threshold)
    feedback = evaluator.evaluate(
        expected_text=expected_text,
        actual_text=transcript_text,
        pronunciation_scores=pronunciation_scores,
    )

    print(f"Doğruluk skoru: {feedback.accuracy_score:.2f}%")
    print("Eşleşen kelimeler:", ", ".join(feedback.matched_words) or "-")
    print("Eksik kelimeler:", ", ".join(feedback.missing_words) or "-")
    print("Fazla kelimeler:", ", ".join(feedback.extra_words) or "-")
    print("Telaffuzda güçlükler:", ", ".join(feedback.mispronounced_words) or "-")
    print("Öneriler:")
    for suggestion in feedback.suggestions:
        print(f"- {suggestion}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
