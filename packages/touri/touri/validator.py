from __future__ import annotations

from pathlib import Path
from typing import Any

import json

from .loader import load_manifest


def validate_manifest(path: str | Path) -> dict[str, Any]:
    manifest = load_manifest(path)
    warnings: list[str] = []
    errors: list[str] = []
    if manifest.policy.get("requires_approval") is None and manifest.capability.kind == "command":
        warnings.append("command capability should define policy.requires_approval")
    if manifest.backend.type == "python" and not manifest.backend.target:
        errors.append("python backend requires backend.target")
    if manifest.backend.type == "shell" and not manifest.backend.command:
        errors.append("shell backend requires backend.command")
    if manifest.backend.type == "http" and not manifest.backend.url:
        errors.append("http backend requires backend.url")
    if manifest.backend.type == "uri_flow" and not manifest.backend.flow:
        errors.append("uri_flow backend requires backend.flow")
    if manifest.backend.type == "uri_graph" and not manifest.backend.graph:
        errors.append("uri_graph backend requires backend.graph")
    if manifest.backend.type == "uri2ops" and manifest.capability.scheme not in {"browser", "dom", "screen", "input", "android", "pcwin"}:
        warnings.append("uri2ops backend is intended for operator schemes (browser/dom/screen/input/android/pcwin)")
    return {"ok": not errors, "errors": errors, "warnings": warnings, "capability": manifest.capability.id}
