"""Severity utilities for normalizing model outputs."""
from __future__ import annotations

from enum import Enum


class Severity(str, Enum):
    """Standard severity scale for security incidents."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


_SEVERITY_ORDER = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]


def normalize_severity(text: str) -> Severity:
    """Normalize free-form severity text to a :class:`Severity` value.

    The function searches for known severity keywords in the provided text, ignoring
    case. If no match is found, ``Severity.MEDIUM`` is returned as a safe default.
    """

    lowered = text.lower()
    for level in _SEVERITY_ORDER:
        if level.value.lower() in lowered:
            return level
    return Severity.MEDIUM
