"""Utilities for preparing Arabic text for evaluation."""

from __future__ import annotations

import re
from typing import Iterable, List

# Arabic diacritic marks and Quran-specific annotations to remove during normalization.
_DIACRITICS_PATTERN = re.compile(
    r"[\u0610-\u061A\u064B-\u065F\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]"
)
# General punctuation marks except apostrophes inside words.
_PUNCTUATION_PATTERN = re.compile(r"[\u2000-\u206F\u2E00-\u2E7F`~!@#$%^&*()_+=\[{\]}\\|;:'\",<.>/?-]")


def strip_diacritics(text: str) -> str:
    """Remove Quranic diacritics and annotation symbols from ``text``."""
    return _DIACRITICS_PATTERN.sub("", text)


def normalize_text(text: str) -> str:
    """Normalize Arabic text for comparison.

    The normalization removes diacritics, collapses whitespace and strips out
    punctuation that does not affect pronunciation. It preserves Arabic letters
    and digits.
    """

    text = strip_diacritics(text)
    text = _PUNCTUATION_PATTERN.sub(" ", text)
    text = re.sub(r"\s+", " ", text, flags=re.UNICODE)
    return text.strip()


def tokenize(text: str) -> List[str]:
    """Split normalized text into individual word tokens."""
    if not text:
        return []
    return text.split()


def normalize_tokens(tokens: Iterable[str]) -> List[str]:
    """Normalize and tokenize an iterable of raw tokens."""
    normalized = [normalize_text(token) for token in tokens]
    return [token for token in normalized if token]
