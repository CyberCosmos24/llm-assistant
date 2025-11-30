from __future__ import annotations

from typing import Any, Dict, List

from analysis.severity import Severity, normalize_severity
from llm.client import chat
from llm.prompts import build_multi_log_prompt, build_single_log_prompt


def analyze_single_event(event: Dict[str, Any]) -> Dict[str, Any]:
    prompt = build_single_log_prompt(event)
    raw_response = chat(prompt)
    severity = normalize_severity(raw_response)
    return {
        "explanation": raw_response,
        "severity": severity,
        "raw_response": raw_response,
    }


def analyze_multiple_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    prompt = build_multi_log_prompt(events)
    raw_response = chat(prompt)
    severity = normalize_severity(raw_response)
    top_events: List[Dict[str, Any]] = events[:3] if events else []
    return {
        "summary": raw_response,
        "top_events": top_events,
        "severity": severity,
        "raw_response": raw_response,
    }
