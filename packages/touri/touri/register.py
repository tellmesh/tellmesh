from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

from .loader import load_manifest
from .validator import validate_manifest


def sample_uri_from_template(template: str) -> str:
    defaults = {
        "place": "Gdansk",
        "days": "14",
        "name": "sample",
        "id": "sample",
    }

    def repl(match: re.Match[str]) -> str:
        return defaults.get(match.group(1), "sample")

    return re.sub(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", repl, template)


def register_capability(
    manifest_path: str | Path,
    *,
    registry_root: str | Path,
    install: bool = False,
    root: Path | None = None,
) -> dict[str, Any]:
    path = Path(manifest_path)
    validation = validate_manifest(path)
    if not validation["ok"]:
        return {"ok": False, **validation}

    registry = Path(registry_root)
    registry.mkdir(parents=True, exist_ok=True)
    installed_path = registry / path.name
    if install:
        shutil.copy2(path, installed_path)
        manifest_file = installed_path
    else:
        manifest_file = path.resolve()

    manifest = load_manifest(manifest_file)
    sample_uri = sample_uri_from_template(manifest.capability.uri_template)

    explain: dict[str, Any] | None = None
    try:
        from uri3.resolvers.explain import explain_uri

        explain = explain_uri(sample_uri, registry_root=registry, root=root)
    except ImportError:
        explain = {"note": "uri3 not available for explain check"}

    matched = explain.get("matched_registry") == "touri" if explain else False
    return {
        "ok": matched,
        "capability": manifest.capability.id,
        "scheme": manifest.capability.scheme,
        "uri_template": manifest.capability.uri_template,
        "sample_uri": sample_uri,
        "manifest": str(manifest_file),
        "registry": str(registry),
        "installed": install,
        "validation": validation,
        "explain": explain,
        "warnings": validation.get("warnings") or [],
    }
