from __future__ import annotations

from pathlib import Path
from typing import Any


def _default_transcript() -> str:
    return "wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"


def transcribe(payload: dict[str, Any] | None = None, context: dict[str, Any] | None = None):
    del context
    payload = payload or {}

    text = payload.get("text")
    transcript_file = payload.get("transcript_file")

    if not text and transcript_file:
        text = Path(transcript_file).read_text(encoding="utf-8").strip()

    if not text:
        text = _default_transcript()

    return {
        "ok": True,
        "result_type": "transcript",
        "data": {
            "text": text,
            "language": payload.get("language", "pl"),
        },
        "meta": {
            "engine": "mock",
            "audio_uri": payload.get("audio_uri"),
        },
    }
