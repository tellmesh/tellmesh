from __future__ import annotations

import json
from typing import Any

from agents.operators.desktop_operator.adapters.android_uri import device_id_from_payload
from uri2ops.operator.artifacts import mock_screenshot_png, write_step_artifact


def _task_context(context: dict[str, Any] | None) -> tuple[str, str, str | None]:
    ctx = context or {}
    return str(ctx.get("task_id") or "task"), str(ctx.get("run_id") or "run"), ctx.get("root")


def screenshot(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = device_id_from_payload(payload)
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "screenshot")
    meta = {"ok": True, "device_id": device_id, "mock": True, "width": 1080, "height": 1920}
    png = mock_screenshot_png(width=360, height=640)
    _, artifact_uri = write_step_artifact(
        task_id,
        run_id,
        step_id,
        "screenshot.png",
        png,
        root=root,
    )
    return {**meta, "artifact_uri": artifact_uri, "screenshot_uri": artifact_uri}


def dump_ui(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = device_id_from_payload(payload)
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "dump_ui")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<hierarchy><node class="android.widget.FrameLayout" text="" bounds="[0,0][1080,1920]">'
        '<node class="android.widget.TextView" text="Settings" resource-id="com.android.settings:id/title" '
        'bounds="[40,120][300,180]" clickable="true"/></node></hierarchy>'
    )
    meta = {"ok": True, "device_id": device_id, "mock": True, "node_count": 2, "xml": xml}
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "ui_dump.xml", xml, root=root)
    return {**meta, "artifact_uri": artifact_uri}


def tap(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = device_id_from_payload(payload)
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "tap")
    x = payload.get("x")
    y = payload.get("y")
    selector = payload.get("selector")
    meta = {"ok": True, "device_id": device_id, "mock": True, "x": x, "y": y, "selector": selector}
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "tap.json", json.dumps(meta, indent=2), root=root)
    return {**meta, "artifact_uri": artifact_uri}
