from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from agents.operators.desktop_operator.adapters.android_uri import device_id_from_payload
from uri2ops.operator.artifacts import write_step_artifact

REMOTE_DUMP = "/sdcard/uri2ops_window_dump.xml"


def _task_context(context: dict[str, Any] | None) -> tuple[str, str, str | None]:
    ctx = context or {}
    return str(ctx.get("task_id") or "task"), str(ctx.get("run_id") or "run"), ctx.get("root")


def _run_adb(device_id: str, *args: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    command = ["adb", "-s", device_id, *args]
    return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)


def adb_available() -> bool:
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True, timeout=5, check=False)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def device_ready(device_id: str) -> bool:
    if not adb_available():
        return False
    result = _run_adb(device_id, "get-state")
    return result.returncode == 0 and result.stdout.strip() == "device"


def list_devices() -> list[str]:
    if not adb_available():
        return []
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5, check=False)
    if result.returncode != 0:
        return []
    devices: list[str] = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def screenshot(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = device_id_from_payload(payload)
    if not device_ready(device_id):
        return {"ok": False, "error": f"adb device not ready: {device_id!r}"}
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "screenshot")
    result = subprocess.run(
        ["adb", "-s", device_id, "exec-out", "screencap", "-p"],
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode != 0 or not result.stdout:
        return {"ok": False, "error": result.stderr.strip() or "screencap failed"}
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "screenshot.png", result.stdout, root=root)
    return {
        "ok": True,
        "device_id": device_id,
        "artifact_uri": artifact_uri,
        "screenshot_uri": artifact_uri,
        "bytes": len(result.stdout),
    }


def dump_ui(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = device_id_from_payload(payload)
    if not device_ready(device_id):
        return {"ok": False, "error": f"adb device not ready: {device_id!r}"}
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "dump_ui")
    dump_result = _run_adb(device_id, "shell", "uiautomator", "dump", REMOTE_DUMP)
    if dump_result.returncode != 0:
        return {"ok": False, "error": dump_result.stderr.strip() or "uiautomator dump failed"}
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as handle:
        local_path = Path(handle.name)
    pull_result = _run_adb(device_id, "pull", REMOTE_DUMP, str(local_path))
    if pull_result.returncode != 0:
        return {"ok": False, "error": pull_result.stderr.strip() or "adb pull failed"}
    xml = local_path.read_text(encoding="utf-8", errors="replace")
    local_path.unlink(missing_ok=True)
    _run_adb(device_id, "shell", "rm", "-f", REMOTE_DUMP)
    node_count = xml.count("<node ")
    meta = {"ok": True, "device_id": device_id, "node_count": node_count, "xml": xml}
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "ui_dump.xml", xml, root=root)
    return {**meta, "artifact_uri": artifact_uri}


def tap(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = device_id_from_payload(payload)
    if not device_ready(device_id):
        return {"ok": False, "error": f"adb device not ready: {device_id!r}"}
    x = payload.get("x")
    y = payload.get("y")
    selector = payload.get("selector")
    if selector:
        dump = dump_ui(payload, context)
        if not dump.get("ok"):
            return dump
        xml = str(dump.get("xml") or "")
        bounds = _find_selector_bounds(xml, str(selector))
        if bounds is None:
            return {"ok": False, "error": f"selector not found: {selector!r}"}
        x, y = bounds
    if x is None or y is None:
        return {"ok": False, "error": "tap requires x/y coordinates or selector"}
    tap_result = _run_adb(device_id, "shell", "input", "tap", str(int(x)), str(int(y)))
    if tap_result.returncode != 0:
        return {"ok": False, "error": tap_result.stderr.strip() or "input tap failed"}
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "tap")
    meta = {"ok": True, "device_id": device_id, "x": int(x), "y": int(y), "selector": selector}
    _, artifact_uri = write_step_artifact(task_id, run_id, step_id, "tap.json", json.dumps(meta, indent=2), root=root)
    return {**meta, "artifact_uri": artifact_uri}


def _find_selector_bounds(xml: str, selector: str) -> tuple[int, int] | None:
    import re

    patterns = [
        rf'resource-id="{re.escape(selector)}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
        rf'text="{re.escape(selector)}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
        rf'content-desc="{re.escape(selector)}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"',
    ]
    for pattern in patterns:
        match = re.search(pattern, xml)
        if match:
            x1, y1, x2, y2 = (int(match.group(i)) for i in range(1, 5))
            return (x1 + x2) // 2, (y1 + y2) // 2
    return None
