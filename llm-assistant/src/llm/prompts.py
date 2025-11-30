"""Prompt builders for the local cybersecurity assistant."""
from __future__ import annotations

import json
from typing import List, Dict

SEVERITY_SCALE = "LOW, MEDIUM, HIGH, CRITICAL"


def _format_event(event: dict) -> str:
    """Return a JSON string representation of an event for inclusion in prompts."""
    return json.dumps(event, ensure_ascii=False, indent=2)


def build_single_log_prompt(log_event: Dict) -> str:
    """Construct a prompt asking the LLM to explain a single log event."""
    event_repr = _format_event(log_event)
    return (
        "You are a cybersecurity assistant. Given the following log entry, explain in plain "
        "English what happened. Provide a severity rating from the following set: "
        f"{SEVERITY_SCALE}. Include a brief bullet list of reasons supporting the severity.\n\n"
        f"Log Entry:\n{event_repr}\n\n"
        "Respond with the explanation, the severity label, and the bullet-point reasoning."
    )


def build_multi_log_prompt(log_events: List[Dict]) -> str:
    """Construct a prompt asking the LLM to summarize multiple log events."""
    formatted_events = "\n\n".join(_format_event(event) for event in log_events)
    return (
        "You are a cybersecurity assistant. Review the following log entries and summarize "
        "the incident in plain English. Identify the most significant events and rate the overall "
        f"severity as one of: {SEVERITY_SCALE}. Provide a short bullet list explaining your reasoning.\n\n"
        f"Log Entries:\n{formatted_events}\n\n"
        "Respond with a concise summary, the chosen severity label, and bullet-point reasoning."
    )
