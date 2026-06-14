from __future__ import annotations

# Re-export for tests and backward-compatible imports.
from uri2pact.core import (  # noqa: F401
    extract_markpact_blocks,
    find_repo_root,
    is_markpact_registry,
    resolve_markpact_ref,
)
from uri2pact.flows import load_markpact_flow_dict

is_markpact_flow_ref = is_markpact_registry
load_markpact_flow = load_markpact_flow_dict

__all__ = [
    "extract_markpact_blocks",
    "find_repo_root",
    "is_markpact_flow_ref",
    "is_markpact_registry",
    "load_markpact_flow",
    "load_markpact_flow_dict",
    "resolve_markpact_ref",
]
