from __future__ import annotations

from pathlib import Path

from .loaders.registry_loader import load_registry as _load_registry
from .manifest import load_manifest, load_manifest_from_dict


def iter_manifest_paths(root: str | Path):
    from .loaders.file_loader import iter_manifest_paths as _iter

    yield from _iter(root)


def load_registry(root: str | Path):
    return _load_registry(root)


__all__ = [
    "iter_manifest_paths",
    "load_manifest",
    "load_manifest_from_dict",
    "load_registry",
]
