from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from uri2ops.operator.artifacts import write_step_artifact


def gnome_available() -> bool:
    if not os.getenv("DISPLAY") and not os.getenv("WAYLAND_DISPLAY"):
        return False
    return bool(shutil.which("gnome-screenshot") or shutil.which("grim") or shutil.which("scrot"))


def _task_context(context: dict[str, Any] | None) -> tuple[str, str, str | None]:
    ctx = context or {}
    return str(ctx.get("task_id") or "task"), str(ctx.get("run_id") or "run"), ctx.get("root")


def observe(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    if not gnome_available():
        return {
            "ok": False,
            "error": "GNOME/Linux desktop adapter requires DISPLAY/WAYLAND_DISPLAY and gnome-screenshot, grim, or scrot",
        }
    task_id, run_id, root = _task_context(context)
    step_id = str(payload.get("step_id") or "screen_observe")
    temp_path = Path(root or ".") / "output" / "artifacts" / "operator" / "tmp" / f"{step_id}.png"
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    ok, detail = _capture_screenshot(temp_path)
    if not ok:
        hint = detail or f"desktop screenshot failed for {temp_path}"
        if not os.getenv("DISPLAY") and not os.getenv("WAYLAND_DISPLAY"):
            hint = (
                f"{hint}; desktop-operator needs DISPLAY/WAYLAND_DISPLAY "
                "(restart with: hypervisor run-agent desktop-operator.local --detach --if-running restart "
                "and export DISPLAY=:0)"
            )
        return {"ok": False, "error": hint}
    image = temp_path.read_bytes()
    path, artifact_uri = write_step_artifact(
        task_id,
        run_id,
        step_id,
        "screenshot.png",
        image,
        root=root,
    )
    windows = _list_windows()
    meta = {
        "ok": True,
        "target_uri": payload.get("target_uri"),
        "screenshot_path": str(path),
        "desktop_session": os.getenv("XDG_CURRENT_DESKTOP") or os.getenv("DESKTOP_SESSION") or "linux",
        "windows": windows,
    }
    _, meta_uri = write_step_artifact(
        task_id,
        run_id,
        step_id,
        "observe.json",
        json.dumps(meta, ensure_ascii=False, indent=2),
        root=root,
    )
    return {
        "ok": True,
        "screenshot_uri": artifact_uri,
        "artifact_uri": artifact_uri,
        "meta_artifact_uri": meta_uri,
        "tree_json": json.dumps({"windows": windows}, ensure_ascii=False),
        "meta": meta,
    }


def _desktop_env() -> dict[str, str]:
    env = os.environ.copy()
    uid = os.getuid()
    runtime = os.getenv("XDG_RUNTIME_DIR") or f"/run/user/{uid}"
    env.setdefault("XDG_RUNTIME_DIR", runtime)
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", f"unix:path={runtime}/bus")
    for key in ("DISPLAY", "WAYLAND_DISPLAY", "XAUTHORITY"):
        value = os.getenv(key)
        if value:
            env[key] = value
    return env


def _capture_screenshot(target: Path) -> tuple[bool, str]:
    env = _desktop_env()
    if os.getenv("WAYLAND_DISPLAY") and shutil.which("grim"):
        result = subprocess.run(["grim", str(target)], capture_output=True, text=True, check=False, env=env)
        if result.returncode == 0 and target.is_file():
            return True, ""
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail or f"grim exited {result.returncode}"
    if shutil.which("gnome-screenshot"):
        result = subprocess.run(
            ["gnome-screenshot", f"--file={target}"],
            capture_output=True,
            text=True,
            check=False,
            env=env,
        )
        if result.returncode == 0 and target.is_file():
            return True, ""
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail or f"gnome-screenshot exited {result.returncode}"
    if shutil.which("grim"):
        result = subprocess.run(["grim", str(target)], capture_output=True, text=True, check=False, env=env)
        if result.returncode == 0 and target.is_file():
            return True, ""
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail or f"grim exited {result.returncode}"
    if shutil.which("scrot"):
        result = subprocess.run(["scrot", str(target)], capture_output=True, text=True, check=False, env=env)
        if result.returncode == 0 and target.is_file():
            return True, ""
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail or f"scrot exited {result.returncode}"
    return False, "no screenshot tool available"


def _list_windows() -> list[dict[str, str]]:
    if not shutil.which("wmctrl"):
        return []
    result = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return []
    windows: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        windows.append({"id": parts[0], "desktop": parts[1], "host": parts[2], "title": parts[3]})
    return windows
