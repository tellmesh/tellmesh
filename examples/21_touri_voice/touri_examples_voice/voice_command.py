from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _artifact_dir(context: dict[str, Any] | None) -> Path:
    root = Path((context or {}).get("root") or ".")
    out_dir = root / "output" / "artifacts" / "voice"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def plan_voice_command(
    payload: dict[str, Any] | None = None,
    context: dict[str, Any] | None = None,
):
    payload = payload or {}
    text = str(payload.get("text") or "").strip()

    if not text:
        return {
            "ok": False,
            "result_type": "error",
            "errors": [{"code": "EMPTY_TEXT", "detail": "Missing voice command text"}],
        }

    try:
        from nl2uri.flow_planner import plan_flow
    except ImportError as exc:
        return {
            "ok": False,
            "result_type": "error",
            "errors": [{"code": "NL2URI_UNAVAILABLE", "detail": str(exc)}],
        }

    try:
        flow_payload = plan_flow(text)
        flow_yaml = yaml.safe_dump(flow_payload, sort_keys=False, allow_unicode=True)
    except Exception as exc:
        return {
            "ok": False,
            "result_type": "error",
            "errors": [{"code": "NL2URI_FAILED", "detail": str(exc)}],
        }

    out_dir = _artifact_dir(context)
    out_file = out_dir / "voice_command.uri.flow.yaml"
    out_file.write_text(flow_yaml, encoding="utf-8")

    return {
        "ok": True,
        "result_type": "uri_flow",
        "data": {
            "text": text,
            "flow_yaml": flow_yaml,
            "flow_file": str(out_file),
            "flow_id": (flow_payload.get("flow") or {}).get("id"),
        },
        "artifact_uri": "artifact://voice/voice_command.uri.flow.yaml",
        "meta": {
            "planner": "nl2uri",
        },
    }
