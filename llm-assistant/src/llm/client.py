from __future__ import annotations

from typing import Final

import requests

DEFAULT_MODEL: Final[str] = "llama3.1"


def chat(prompt: str, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    response = requests.post("http://localhost:11434/api/chat", json=payload)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]
