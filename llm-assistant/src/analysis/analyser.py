"""Compatibility shim for the primary analyzer module."""
from __future__ import annotations

from analysis.analyzer import analyze_multiple_events, analyze_single_event

__all__ = ["analyze_single_event", "analyze_multiple_events"]
