from __future__ import annotations

from pathlib import Path


def repo_www_dir() -> Path | None:
    """Return TellMesh www/ for static UI (hypervisor www/ or tellmesh/www checkout)."""
    try:
        from hypervisor.paths import resolve_www_dir

        return resolve_www_dir(Path(__file__).resolve())
    except Exception:  # noqa: BLE001
        return None
