from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml

from ..manifest import load_manifest_from_dict
from ..models import CapabilityManifest

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


def _block_capability_id(block: dict[str, Any], data: dict[str, Any]) -> str:
    cap = data.get("capability") or {}
    cap_id = cap.get("id")
    if cap_id:
        return str(cap_id)
    if block.get("meta"):
        return str(block["meta"])
    raise ValueError("markpact:capability block missing capability.id and meta id")


def _load_capability_block(block: dict[str, Any], *, source: str) -> CapabilityManifest:
    data = yaml.safe_load(block["body"]) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in markpact:capability block ({source})")
    cap_id = _block_capability_id(block, data)
    return load_manifest_from_dict(data, source=f"{source}#{cap_id}")


def load_markpact_capabilities(
    ref: str | Path,
    *,
    root: Path | None = None,
) -> list[CapabilityManifest]:
    """Load capability manifests from ``markpact://path/to/README.md[#capability.id]``."""
    readme_path, fragment = resolve_markpact_ref(ref, root=root)
    markdown = readme_path.read_text(encoding="utf-8")
    blocks = extract_markpact_blocks(markdown, "capability")
    if not blocks:
        raise ValueError(f"No markpact:capability blocks found in {readme_path}")

    manifests: list[CapabilityManifest] = []
    for block in blocks:
        manifest = _load_capability_block(block, source=str(readme_path))
        cap_id = manifest.capability.id
        meta_id = (block.get("meta") or "").strip()
        if fragment and cap_id != fragment and meta_id != fragment:
            continue
        manifests.append(manifest)

    if fragment and not manifests:
        raise ValueError(
            f"No markpact:capability block matching #{fragment} in {readme_path}"
        )
    return manifests
