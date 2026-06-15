from __future__ import annotations

from typing import Any

from uri2ops.operator.artifacts import write_artifact


def _path_parts(target_uri: str) -> list[str]:
    from urllib.parse import urlparse

    parsed = urlparse(target_uri)
    combined = f"{parsed.netloc}/{parsed.path.lstrip('/')}" if parsed.netloc else parsed.path
    return [part for part in combined.split("/") if part]


def _target_id(payload: dict[str, Any], fallback: str) -> str:
    parts = _path_parts(str(payload.get("target_uri") or ""))
    if len(parts) >= 2 and parts[0] in {"robot", "device"}:
        return parts[1]
    return str(payload.get("id") or payload.get("target_id") or fallback)


def robot_state(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    robot_id = _target_id(payload, "robot-1")
    state = {
        "ok": True,
        "robot_id": robot_id,
        "mode": "mock",
        "status": "idle",
        "battery_pct": 87,
        "pose": {"x": 0.0, "y": 0.0, "theta": 0.0},
        "safety": {"estop": False, "protective_stop": False},
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "robot_state"), state)
    return {**state, "artifact_uri": artifact_uri}


def robot_move(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    robot_id = _target_id(payload, "robot-1")
    target = payload.get("target") or {
        "x": payload.get("x", 0),
        "y": payload.get("y", 0),
        "theta": payload.get("theta", 0),
    }
    command = {
        "ok": True,
        "robot_id": robot_id,
        "mode": "mock",
        "command": "move",
        "accepted": True,
        "target": target,
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "robot_move"), command)
    return {**command, "artifact_uri": artifact_uri}


def robot_stop(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    robot_id = _target_id(payload, "robot-1")
    command = {
        "ok": True,
        "robot_id": robot_id,
        "mode": "mock",
        "command": "stop",
        "accepted": True,
        "safety_state": "stopped",
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "robot_stop"), command)
    return {**command, "artifact_uri": artifact_uri}


def robot_mission_start(
    payload: dict[str, Any],
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    robot_id = _target_id(payload, "robot-1")
    parts = _path_parts(str(payload.get("target_uri") or ""))
    mission_id = str(payload.get("mission_id") or (parts[3] if len(parts) >= 4 else "mission-1"))
    command = {
        "ok": True,
        "robot_id": robot_id,
        "mission_id": mission_id,
        "mode": "mock",
        "command": "mission_start",
        "accepted": True,
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "robot_mission_start"), command)
    return {**command, "artifact_uri": artifact_uri}


def device_status(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = _target_id(payload, "device-1")
    status = {
        "ok": True,
        "device_id": device_id,
        "mode": "mock",
        "online": True,
        "health": "ok",
        "protocol": payload.get("protocol") or "mock",
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "device_status"), status)
    return {**status, "artifact_uri": artifact_uri}


def device_read(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = _target_id(payload, "device-1")
    channel = str(payload.get("channel") or payload.get("register") or "default")
    value = payload.get("value", 42)
    reading = {
        "ok": True,
        "device_id": device_id,
        "mode": "mock",
        "channel": channel,
        "value": value,
        "unit": payload.get("unit"),
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "device_read"), reading)
    return {**reading, "artifact_uri": artifact_uri}


def device_write(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    device_id = _target_id(payload, "device-1")
    channel = str(payload.get("channel") or payload.get("register") or "default")
    command = {
        "ok": True,
        "device_id": device_id,
        "mode": "mock",
        "command": "write",
        "channel": channel,
        "value": payload.get("value"),
        "accepted": True,
    }
    artifact_uri = write_artifact(str(payload.get("step_id") or "device_write"), command)
    return {**command, "artifact_uri": artifact_uri}
