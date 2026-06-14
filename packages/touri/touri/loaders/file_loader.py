from __future__ import annotations

from pathlib import Path

from ..manifest import load_manifest
from ..models import CapabilityManifest


def iter_manifest_paths(root: str | Path):
    r = Path(root)
    if r.is_file():
        yield r
        return
    yield from sorted(r.rglob("*.uri.capability.yaml"))


def load_file_registry(root: str | Path) -> list[CapabilityManifest]:
    return [load_manifest(path) for path in iter_manifest_paths(root)]
