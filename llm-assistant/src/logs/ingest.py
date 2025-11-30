"""Utilities for loading log files from disk."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

try:  # Prefer ujson if available for speed
    import ujson as _json
except ModuleNotFoundError:  # pragma: no cover - fallback to stdlib
    _json = json


def load_json_logs(path: str) -> List[Dict]:
    """Load JSON log records from a file.

    The function attempts to parse the file as a list of JSON objects or a single
    JSON object. Invalid files or parsing errors return an empty list instead of
    raising an exception.
    """

    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            data = _json.load(handle)
    except (OSError, ValueError):
        return []

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def load_text_logs(path: str) -> List[str]:
    """Load plain-text log lines from a file.

    Missing files or read errors return an empty list. Lines are stripped of
    trailing whitespace and empty lines are ignored.
    """

    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            lines = [line.rstrip() for line in handle if line.strip()]
    except OSError:
        return []

    return lines
