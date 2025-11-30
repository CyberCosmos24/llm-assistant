from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests


def _ensure_output_path(output_path: Path | None) -> Path:
    directory = Path(__file__).resolve().parents[2] / "data" / "logs" / "cloudflare"
    directory.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        timestamp = int(datetime.now(timezone.utc).timestamp())
        output_path = directory / f"cloudflare_{timestamp}.jsonl"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def _default_time_window(start: str | None, end: str | None) -> tuple[str, str]:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    end_ts = end or now.isoformat()
    start_ts = start or (now - timedelta(minutes=60)).isoformat()
    return start_ts, end_ts


def fetch_cloudflare_logs(
    zone_id: str,
    api_token: str,
    start: str | None = None,
    end: str | None = None,
    limit: int = 100,
    output_path: Path | None = None,
) -> Tuple[Path, List[Dict[str, Any]]]:
    start_ts, end_ts = _default_time_window(start, end)
    headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    query = """
    query FirewallEvents($zoneTag: String!, $filter: FirewallEventsAdaptiveFilter_InputObject, $limit: Int!) {
      viewer {
        zones(filter: { zoneTag: $zoneTag }) {
          firewallEventsAdaptive(filter: $filter, limit: $limit, orderBy: [datetime_DESC]) {
            action
            datetime
            clientIP
            clientCountryName
            clientRequestHTTPHost
            clientRequestPath
            clientRequestQuery
            userAgent
            ruleId
            source
          }
        }
      }
    }
    """
    variables = {
        "zoneTag": zone_id,
        "filter": {"datetime_geq": start_ts, "datetime_leq": end_ts},
        "limit": limit,
    }
    response = requests.post(
        "https://api.cloudflare.com/client/v4/graphql",
        headers=headers,
        json={"query": query, "variables": variables},
        timeout=60,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()
    errors = payload.get("errors")
    if errors:
        raise RuntimeError(f"Cloudflare GraphQL returned errors: {errors}")
    zones = payload.get("data", {}).get("viewer", {}).get("zones", [])
    events = []
    if zones and isinstance(zones[0], dict):
        events = zones[0].get("firewallEventsAdaptive", []) or []
    destination = _ensure_output_path(output_path)
    with destination.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, ensure_ascii=False))
            handle.write("\n")
    return destination, events
