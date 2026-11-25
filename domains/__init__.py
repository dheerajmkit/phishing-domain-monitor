"""Phishing domain (typosquat) monitor."""

from .typosquat import variants
from .scoring import score, levenshtein
from .report import render_text, render_json

__all__ = ["variants", "score", "levenshtein",
           "render_text", "render_json"]
