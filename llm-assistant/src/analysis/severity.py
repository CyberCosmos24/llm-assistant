from __future__ import annotations

import re
from enum import Enum


class Severity(str, Enum):
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
    for level in _ORDERED_LEVELS:
        pattern = _SEVERITY_PATTERNS[level]
        if pattern.search(text):
            return level
    return Severity.MEDIUM
