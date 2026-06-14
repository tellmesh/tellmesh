from __future__ import annotations

from pathlib import Path

from uri3.config.repo_root import find_repo_root


def project_root() -> Path:
    return find_repo_root()


__all__ = ["find_repo_root", "project_root"]
