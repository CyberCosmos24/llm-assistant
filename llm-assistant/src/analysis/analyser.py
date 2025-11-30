"""Analysis helpers that delegate reasoning to the LLM."""
from __future__ import annotations

from typing import Dict, List, Any

from llm.client import chat
from llm.prompts import build_single_log_prompt, build_multi_log_prompt
from analysis.severity import normalize_severity


def analyze_single_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a single log event using the language model."""

    prompt = build_single_log_prompt(event)
    raw_response = chat(prompt)
    severity = normalize_severity(raw_response)

    return {
        "explanation": raw_response,
        "severity": severity,
        "raw_response": raw_response,
    }


def analyze_multiple_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze multiple log events and produce a consolidated summary."""

    prompt = build_multi_log_prompt(events)
    raw_response = chat(prompt)
    severity = normalize_severity(raw_response)

    return {
        "summary": raw_response,
        "top_events": events[:3],
        "severity": severity,
        "raw_response": raw_response,
    }
