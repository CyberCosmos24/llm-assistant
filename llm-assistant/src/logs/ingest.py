from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

try:
    import ujson as _json
except ModuleNotFoundError:
    _json = json


def load_json_logs(path: str) -> List[Dict]:
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
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return []
    try:
        with file_path.open("r", encoding="utf-8") as handle:
            lines = [line.rstrip() for line in handle if line.strip()]
    except OSError:
        return []
    return lines
