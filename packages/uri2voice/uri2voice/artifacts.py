from __future__ import annotations

from pathlib import Path
from typing import Any


def voice_artifact_dir(context: dict[str, Any] | None) -> Path:
    root = Path((context or {}).get("root") or ".")
    out_dir = root / "output" / "artifacts" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir
