from __future__ import annotations

import json
from typing import Any

from agents.operators.desktop_operator.adapters.pcwin_uri import automation_id_from_payload, window_id_from_payload
from uri2ops.operator.artifacts import write_step_artifact


def _task_context(context: dict[str, Any] | None) -> tuple[str, str, str | None]:
    ctx = context or {}
    return str(ctx.get("task_id") or "task"), str(ctx.get("run_id") or "run"), ctx.get("root")


def focus(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    window_id = window_id_from_payload(payload)
    title = str(payload.get("title") or window_id)
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "focus")
    meta = {"ok": True, "mock": True, "window_id": window_id, "title": title, "focused": True}
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "focus.json", json.dumps(meta, indent=2), root=root)
    return {**meta, "artifact_uri": artifact_uri}


def click(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    automation_id = automation_id_from_payload(payload)
    window_id = window_id_from_payload(payload)
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "click")
    meta = {
        "ok": True,
        "mock": True,
        "automation_id": automation_id,
        "window_id": window_id,
        "clicked": True,
    }
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "click.json", json.dumps(meta, indent=2), root=root)
    return {**meta, "artifact_uri": artifact_uri}
