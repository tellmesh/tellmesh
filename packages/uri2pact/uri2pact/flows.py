from __future__ import annotations

from pathlib import Path
from typing import Any

from uri2pact.core import is_markpact_registry, load_markpact_markdown, parse_markpact_yaml_blocks


def load_markpact_flow_dict(
    ref: str | Path,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """Load compact flow YAML from ``markpact://path/to/README.md[#flow.id]``."""
    readme_path, fragment, markdown = load_markpact_markdown(ref, root=root)
    all_blocks = parse_markpact_yaml_blocks(
        markdown,
        "flow",
        fragment=None,
        source=str(readme_path),
    )
    if not all_blocks:
        raise ValueError(f"No markpact:flow blocks found in {readme_path}")
    matches = parse_markpact_yaml_blocks(
        markdown,
        "flow",
        fragment=fragment,
        source=str(readme_path),
    )
    if fragment and not matches:
        raise ValueError(f"No markpact:flow block matching #{fragment} in {readme_path}")
    if not fragment and len(all_blocks) > 1:
        raise ValueError(
            f"Multiple markpact:flow blocks in {readme_path}; specify #flow.id fragment"
        )
    return (matches or all_blocks)[0][1]


is_markpact_flow_ref = is_markpact_registry
load_markpact_flow = load_markpact_flow_dict
