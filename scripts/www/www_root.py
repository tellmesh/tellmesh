"""Resolve TellMesh www/ root for build scripts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_HYPERVISOR_PKG = ROOT / "packages" / "resource-agent-hypervisor"
if str(_HYPERVISOR_PKG) not in sys.path:
    sys.path.insert(0, str(_HYPERVISOR_PKG))


def www_dir() -> Path:
    from hypervisor.paths import resolve_www_dir

    resolved = resolve_www_dir(ROOT)
    return resolved if resolved is not None else ROOT / "www"
