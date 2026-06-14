from __future__ import annotations

from pathlib import Path

from ..models import CapabilityManifest
from .file_loader import load_file_registry
from .markpact_loader import is_markpact_registry, load_markpact_capabilities


def load_registry(root: str | Path) -> list[CapabilityManifest]:
    ref = str(root)
    if is_markpact_registry(ref):
        return load_markpact_capabilities(ref)
    return load_file_registry(ref)
