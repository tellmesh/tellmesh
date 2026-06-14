from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml

MARKPACT_BLOCK_RE = re.compile(
    r"```(?:\w+\s+)?markpact:(?P<kind>\w+)(?:[ \t]+(?P<meta>[^\n]*))?\n(?P<body>[\s\S]*?)\n```",
    re.MULTILINE,
)


def is_markpact_registry(ref: str | Path) -> bool:
    return str(ref).startswith("markpact://")


def _find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for path in (current, *current.parents):
        if (path / "pyproject.toml").is_file() and (path / "examples").is_dir():
            return path
    return current


def resolve_markpact_ref(ref: str | Path, *, root: Path | None = None) -> tuple[Path, str | None]:
    raw = str(ref)
    if not is_markpact_registry(raw):
        raise ValueError(f"Not a markpact registry URI: {raw}")
    target = raw[len("markpact://") :]
    if "#" in target:
        raw_path, fragment = target.split("#", 1)
    else:
        raw_path, fragment = target, None
    path = Path(unquote(raw_path.strip()))
    if not path.is_absolute():
        base = root or _find_repo_root()
        path = base / path
    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"markpact README not found: {resolved} (from {raw})")
    return resolved, (fragment.strip() if fragment else None)


def extract_markpact_blocks(markdown: str, block_type: str) -> list[dict[str, Any]]:
    """Parse fenced ``markpact:<block_type>`` blocks from markdown."""
    blocks: list[dict[str, Any]] = []
    for match in MARKPACT_BLOCK_RE.finditer(markdown):
        kind = match.group("kind")
        if kind != block_type:
            continue
        meta = (match.group("meta") or "").strip()
        body = match.group("body").strip()
        blocks.append({"kind": kind, "meta": meta, "body": body})
    return blocks


def _block_flow_id(block: dict[str, Any], data: dict[str, Any]) -> str:
    flow = data.get("flow") or {}
    flow_id = flow.get("id")
    if flow_id:
        return str(flow_id)
    if block.get("meta"):
        return str(block["meta"])
    raise ValueError("markpact:flow block missing flow.id and meta id")


def load_markpact_flow_dict(
    ref: str | Path,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """Load compact flow YAML from ``markpact://path/to/README.md[#flow.id]``."""
    readme_path, fragment = resolve_markpact_ref(ref, root=root)
    markdown = readme_path.read_text(encoding="utf-8")
    blocks = extract_markpact_blocks(markdown, "flow")
    if not blocks:
        raise ValueError(f"No markpact:flow blocks found in {readme_path}")

    matches: list[dict[str, Any]] = []
    for block in blocks:
        data = yaml.safe_load(block["body"]) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Expected YAML mapping in markpact:flow block ({readme_path})")
        flow_id = _block_flow_id(block, data)
        meta_id = (block.get("meta") or "").strip()
        if fragment and flow_id != fragment and meta_id != fragment:
            continue
        matches.append(data)

    if fragment and not matches:
        raise ValueError(f"No markpact:flow block matching #{fragment} in {readme_path}")
    if not fragment and len(matches) > 1:
        raise ValueError(
            f"Multiple markpact:flow blocks in {readme_path}; specify #flow.id fragment"
        )
    return matches[0]


# Backward-compatible aliases for earlier v0.8.2 draft imports.
is_markpact_flow_ref = is_markpact_registry
load_markpact_flow = load_markpact_flow_dict
