from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests


def _data_directory() -> Path:
    path = Path(__file__).resolve().parents[2] / "data" / "wazuh"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _authenticate(base_url: str, username: str, password: str, verify_ssl: bool) -> str:
    url = f"{base_url.rstrip('/')}/security/user/authenticate"
    response = requests.post(url, auth=(username, password), verify=verify_ssl, timeout=30)
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", {})
    token = data.get("token")
    if not token:
        raise RuntimeError("Authentication failed: token not found in response")
    return token


def fetch_wazuh_alerts(
    base_url: str,
    username: str,
    password: str,
    limit: int = 100,
    verify_ssl: bool = True,
    output_path: Path | None = None,
) -> Tuple[Path, List[Dict[str, Any]]]:
    token = _authenticate(base_url, username, password, verify_ssl)
    alerts_url = f"{base_url.rstrip('/')}/alerts"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": limit}
    response = requests.get(alerts_url, headers=headers, params=params, verify=verify_ssl, timeout=60)
    response.raise_for_status()
    payload = response.json()
    alerts = payload.get("data", payload.get("alerts", []))
    events: List[Dict[str, Any]] = []
    if isinstance(alerts, list):
        events = [item for item in alerts if isinstance(item, dict)]
    elif isinstance(alerts, dict):
        events = [alerts]
    directory = _data_directory()
    if output_path is None:
        timestamp = int(time.time())
        output_path = directory / f"wazuh_alerts_{timestamp}.json"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(alerts, handle, ensure_ascii=False, indent=2)
    return output_path, events
