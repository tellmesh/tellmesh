from __future__ import annotations

from urllib.parse import urlparse


def parse_android_uri(uri: str) -> tuple[str, str | None]:
    """Parse android://device/{device_id}/{action} URIs."""
    parsed = urlparse(uri)
    if parsed.scheme != "android":
        raise ValueError(f"Not an android URI: {uri!r}")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) >= 2 and parts[0] == "device":
        device_id = parts[1]
        action = parts[2] if len(parts) >= 3 else None
        return device_id, action
    if parsed.netloc == "device" and parts:
        return parts[0], parts[1] if len(parts) > 1 else None
    raise ValueError(f"Invalid android URI (expected android://device/{{id}}/{{action}}): {uri!r}")


def device_id_from_payload(payload: dict) -> str:
    target_uri = str(payload.get("target_uri") or "")
    if target_uri.startswith("android://"):
        device_id, _ = parse_android_uri(target_uri)
        return device_id
    return str(payload.get("device_id") or "emulator-5554")
