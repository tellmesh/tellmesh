from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import BackendRef, CapabilityManifest, CapabilityRef

_BACKEND_FIELDS = frozenset(
    {"type", "target", "command", "method", "url", "operation", "flow", "graph"}
)


def _read_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return data


def _parse_capability_block(cap: dict[str, Any], *, label: str) -> CapabilityRef:
    if not cap.get("id") or not cap.get("scheme") or not cap.get("uri_template"):
        raise ValueError(f"Invalid capability block in {label}")
    return CapabilityRef(
        id=str(cap["id"]),
        scheme=str(cap["scheme"]),
        uri_template=str(cap["uri_template"]),
        operation=str(cap.get("operation", "call")),
        kind=str(cap.get("kind", "query")),
        description=str(cap.get("description", "")),
    )


def _parse_backend_block(backend: dict[str, Any], *, label: str) -> BackendRef:
    if not backend.get("type"):
        raise ValueError(f"Invalid backend block in {label}")
    backend_extra = {key: value for key, value in backend.items() if key not in _BACKEND_FIELDS}
    return BackendRef(
        type=str(backend["type"]),
        target=backend.get("target"),
        command=backend.get("command"),
        method=backend.get("method"),
        url=backend.get("url"),
        operation=backend.get("operation"),
        flow=backend.get("flow"),
        graph=backend.get("graph"),
        extra=backend_extra,
    )


def _mapping_block(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value or {}


def _list_block(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    return list(value or [])


def load_manifest_from_dict(data: dict[str, Any], *, source: str = "") -> CapabilityManifest:
    cap = data.get("capability") or {}
    backend = data.get("backend") or {}
    label = source or "manifest"
    return CapabilityManifest(
        version=int(data.get("version", 1)),
        capability=_parse_capability_block(cap, label=label),
        backend=_parse_backend_block(backend, label=label),
        input=_mapping_block(data, "input"),
        output=_mapping_block(data, "output"),
        policy=_mapping_block(data, "policy"),
        events=_mapping_block(data, "events"),
        data_quality=_mapping_block(data, "data_quality"),
        fallbacks=_list_block(data, "fallbacks"),
    )


def load_manifest(path: str | Path) -> CapabilityManifest:
    p = Path(path)
    return load_manifest_from_dict(_read_yaml(p), source=str(p))
