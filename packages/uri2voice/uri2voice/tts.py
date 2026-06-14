from __future__ import annotations

import json
import time
from typing import Any

from uri2voice.artifacts import voice_artifact_dir


def speak(payload: dict[str, Any] | None = None, context: dict[str, Any] | None = None):
    payload = payload or {}
    text = str(payload.get("text") or "")

    out_dir = voice_artifact_dir(context)
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
