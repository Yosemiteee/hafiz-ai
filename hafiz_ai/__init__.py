"""Core package for the Hafız AI project."""

from .data import PASSAGES, Passage, PassageRepository
from .evaluator import RecitationEvaluator, RecitationFeedback

__all__ = [
    "PASSAGES",
    "Passage",
    "PassageRepository",
    "RecitationEvaluator",
    "RecitationFeedback",
]
