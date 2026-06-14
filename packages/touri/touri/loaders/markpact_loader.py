from __future__ import annotations

from pathlib import Path

from uri2pact.capabilities import load_markpact_capability_dicts
from uri2pact.core import extract_markpact_blocks, is_markpact_registry, resolve_markpact_ref

from ..manifest import load_manifest_from_dict
from ..models import CapabilityManifest

__all__ = [
    "extract_markpact_blocks",
    "is_markpact_registry",
    "load_markpact_capabilities",
    "resolve_markpact_ref",
]


def load_markpact_capabilities(
    ref: str | Path,
    *,
    root: Path | None = None,
) -> list[CapabilityManifest]:
    """Load capability manifests from ``markpact://path/to/README.md[#capability.id]``."""
    readme_path, fragment = resolve_markpact_ref(ref, root=root)
    manifests: list[CapabilityManifest] = []
    for data in load_markpact_capability_dicts(ref, root=root):
        cap_id = (data.get("capability") or {}).get("id") or "unknown"
        manifests.append(
            load_manifest_from_dict(data, source=f"{readme_path}#{cap_id}")
        )
    if fragment and not manifests:
        raise ValueError(
            f"No markpact:capability block matching #{fragment} in {readme_path}"
        )
    return manifests
