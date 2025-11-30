"""Severity utilities for normalizing model outputs."""
from __future__ import annotations

import re
from enum import Enum


class Severity(str, Enum):
    """Standard severity scale for security incidents."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


_SEVERITY_PATTERNS = {
    Severity.CRITICAL: re.compile(r"\bcritical\b", re.IGNORECASE),
    Severity.HIGH: re.compile(r"\bhigh\b", re.IGNORECASE),
    Severity.MEDIUM: re.compile(r"\bmedium\b", re.IGNORECASE),
    Severity.LOW: re.compile(r"\blow\b", re.IGNORECASE),
}


_ORDERED_LEVELS = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]


def normalize_severity(text: str) -> Severity:
    """Normalize free-form severity text to a :class:`Severity` value.

    The function searches for known severity keywords in the provided text, ignoring
    case and prioritizing higher severities when multiple are present. If no match
    is found, ``Severity.MEDIUM`` is returned as a safe default.
    """

    for level in _ORDERED_LEVELS:
        pattern = _SEVERITY_PATTERNS[level]
        if pattern.search(text):
            return level
    return Severity.MEDIUM
