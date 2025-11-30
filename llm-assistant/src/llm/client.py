"""Lightweight client for interacting with a local Ollama instance."""
from __future__ import annotations

from typing import Final

import requests

DEFAULT_MODEL: Final[str] = "llama3.1"


def chat(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Send a chat prompt to the local Ollama server and return the response text.

    Args:
        prompt: The text prompt to send to the model.
        model: The model identifier to use when querying Ollama.

    Returns:
        The content of the model's reply.

    Raises:
        requests.HTTPError: If the Ollama server responds with a non-success status.
    """

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    response = requests.post("http://localhost:11434/api/chat", json=payload)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]
