"""
Configuration loader for Hypervisor.

Supports:
- Embedded defaults (hypervisor/data/nlp2uri.yaml)
- User overrides via nlp2uri.yaml next to cwd or XDG config
- Environment variables (HYPERVISOR_* and legacy NLP2URI_*)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from ._version import __version__

DEFAULT_CONFIG_NAME = "nlp2uri.yaml"
PACKAGE_DATA_DIR = Path(__file__).parent / "data"


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def get_default_config() -> dict[str, Any]:
    """Return the embedded default configuration."""
    default_path = PACKAGE_DATA_DIR / DEFAULT_CONFIG_NAME
    cfg = _load_yaml(default_path)
    # ensure hypervisor section
    cfg.setdefault("hypervisor", {})
    cfg["hypervisor"].setdefault("version", __version__)
    return cfg


def load_config(
    path: str | Path | None = None,
    *,
    search_paths: list[Path] | None = None,
) -> dict[str, Any]:
    """
    Load configuration with precedence:
    1. Explicit path (if given)
    2. ./nlp2uri.yaml (cwd)
    3. XDG config dir (~/.config/hypervisor/nlp2uri.yaml or platform equivalent)
    4. Package embedded defaults
    """
    cfg = get_default_config()

    candidates: list[Path] = []
    if path:
        candidates.append(Path(path).expanduser().resolve())

    if search_paths:
        candidates.extend(search_paths)

    # cwd
    candidates.append(Path.cwd() / DEFAULT_CONFIG_NAME)

    # XDG / user config
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        candidates.append(Path(xdg) / "hypervisor" / DEFAULT_CONFIG_NAME)
    else:
        candidates.append(Path.home() / ".config" / "hypervisor" / DEFAULT_CONFIG_NAME)

    for cand in candidates:
        if cand and cand.exists():
            user_cfg = _load_yaml(cand)
            # deep merge (simple top-level + hypervisor section)
            for k, v in user_cfg.items():
                if k == "hypervisor" and isinstance(v, dict):
                    cfg.setdefault("hypervisor", {}).update(v)
                else:
                    cfg[k] = v
            cfg["_config_path"] = str(cand)
            break
    else:
        cfg["_config_path"] = "<embedded-defaults>"

    # env overrides (simple)
    for key in ("platform", "host_platform", "locale", "dry_run", "capture_dir"):
        env_key = f"NLP2URI_{key.upper()}"
        if env_key in os.environ:
            val = os.environ[env_key]
            if key == "dry_run":
                cfg[key] = val.lower() in ("1", "true", "yes", "on")
            else:
                cfg[key] = val

    for key in ("log_level", "max_agents", "default_profile"):
        env_key = f"HYPERVISOR_{key.upper()}"
        if env_key in os.environ:
            cfg.setdefault("hypervisor", {})[key] = os.environ[env_key]

    return cfg


def get_config() -> dict[str, Any]:
    """Return a cached / default-loaded configuration (convenience)."""
    # For v0.1 we do not cache aggressively; call load_config() for fresh merge
    return load_config()
