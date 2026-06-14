from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def _artifact_dir(context: dict[str, Any] | None) -> Path:
    root = Path((context or {}).get("root") or ".")
    out_dir = root / "output" / "artifacts" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def speak(payload: dict[str, Any] | None = None, context: dict[str, Any] | None = None):
    payload = payload or {}
    text = str(payload.get("text") or "")

    out_dir = _artifact_dir(context)
    artifact = out_dir / f"tts_{int(time.time() * 1000)}.json"
    artifact.write_text(
        json.dumps(
            {
                "text": text,
                "voice": payload.get("voice", "mock"),
                "engine": "mock",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    artifact_uri = f"artifact://voice/{artifact.name}"
    return {
        "ok": True,
        "result_type": "artifact",
        "data": {
            "text": text,
            "audio_uri": artifact_uri,
        },
        "artifact_uri": artifact_uri,
        "meta": {
            "engine": "mock",
            "artifact_path": str(artifact),
        },
    }
