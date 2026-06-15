from __future__ import annotations

import os
import shutil
import subprocess
from typing import Any

from uri2ops.operator.artifacts import write_artifact


def gnome_input_available() -> bool:
    if not os.getenv("DISPLAY") and not os.getenv("WAYLAND_DISPLAY"):
        return False
    return bool(shutil.which("ydotool") or shutil.which("xdotool"))


def type_text(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    if not gnome_input_available():
        return {
            "ok": False,
            "error": "GNOME/Linux input adapter requires DISPLAY/WAYLAND_DISPLAY and ydotool or xdotool",
        }
    secret = bool(payload.get("secret", False))
    text = str(payload.get("text") or "")
    if secret:
        redacted = "***"
    else:
        redacted = text
        if shutil.which("ydotool"):
            result = subprocess.run(
                ["ydotool", "type", text],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return {"ok": False, "error": result.stderr.strip() or "ydotool type failed"}
        elif shutil.which("xdotool"):
            result = subprocess.run(
                ["xdotool", "type", "--", text],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                return {"ok": False, "error": result.stderr.strip() or "xdotool type failed"}
    artifact_uri = write_artifact(
        payload.get("step_id", "type_text"),
        {"text": redacted, "secret": secret, "adapter": "gnome"},
    )
    return {"ok": True, "typed": redacted, "artifact_uri": artifact_uri}
