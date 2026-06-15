from __future__ import annotations

from urllib.parse import urlparse

_PCWIN_TARGET_TYPES = frozenset({"window", "control"})


def _pcwin_segments(uri: str) -> list[str]:
    parsed = urlparse(uri)
    if parsed.scheme != "pcwin":
        raise ValueError(f"Not a pcwin URI: {uri!r}")
    segments = [segment for segment in parsed.path.split("/") if segment]
    if parsed.netloc and (not segments or segments[0] not in _PCWIN_TARGET_TYPES):
        segments.insert(0, parsed.netloc)
    return segments


def parse_pcwin_uri(uri: str) -> tuple[str, str, str | None]:
    """Parse pcwin://window/{id}/focus and pcwin://control/{id}/click URIs."""
    segments = _pcwin_segments(uri)
    if len(segments) < 2 or segments[0] not in _PCWIN_TARGET_TYPES:
        raise ValueError(
            "Invalid pcwin URI (expected pcwin://window/{id}/focus or pcwin://control/{id}/click): "
            f"{uri!r}"
        )
    target_type = segments[0]
    target_id = segments[1]
    action = segments[2] if len(segments) > 2 else None
    return target_type, target_id, action


def window_id_from_payload(payload: dict) -> str:
    target_uri = str(payload.get("target_uri") or "")
    if target_uri.startswith("pcwin://"):
        target_type, target_id, _ = parse_pcwin_uri(target_uri)
        if target_type == "window":
            return target_id
    return str(payload.get("window_id") or payload.get("title") or "Notepad")


def automation_id_from_payload(payload: dict) -> str:
    target_uri = str(payload.get("target_uri") or "")
    if target_uri.startswith("pcwin://"):
        target_type, target_id, _ = parse_pcwin_uri(target_uri)
        if target_type == "control":
            return target_id
    return str(payload.get("automation_id") or payload.get("control_id") or "SaveButton")
