from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests


def _ensure_output_path(output_path: Path | None, default_prefix: str) -> Path:
    directory = Path(__file__).resolve().parents[2] / "data" / "cloudflare"
    directory.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        timestamp = int(time.time())
        output_path = directory / f"{default_prefix}_{timestamp}.json"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def fetch_cloudflare_logs(
    zone_id: str,
    api_token: str,
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
    output_path: Path | None = None,
) -> Tuple[Path, List[Dict[str, Any]]]:
    params: Dict[str, Any] = {"limit": limit}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    headers = {"Authorization": f"Bearer {api_token}"}
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/logs/received"
    response = requests.get(url, headers=headers, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    records = payload.get("result", payload.get("data", []))
    events: List[Dict[str, Any]] = []
    if isinstance(records, list):
        events = [item for item in records if isinstance(item, dict)]
    elif isinstance(records, dict):
        events = [records]
    destination = _ensure_output_path(output_path, "cloudflare_logs")
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    return destination, events
