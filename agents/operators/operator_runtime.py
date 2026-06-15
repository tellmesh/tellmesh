from __future__ import annotations

import os
from pathlib import Path

from uri2ops.server.app import create_app


def operator_package_root(module_file: str) -> Path:
    return Path(module_file).resolve().parent


def repo_root_from_operator(module_file: str) -> Path:
    return operator_package_root(module_file).parents[2]


def create_operator_app(
    module_file: str,
    *,
    default_port: int,
    title: str,
    registry_filename: str = "operation_registry.yaml",
) -> object:
    package_root = operator_package_root(module_file)
    registry_path = package_root / registry_filename
    repo = repo_root_from_operator(module_file)
    base_url = os.getenv("URI2OPS_BASE_URL", f"http://127.0.0.1:{default_port}")
    return create_app(
        root=repo,
        base_url=base_url,
        registry_path=registry_path,
        title=title,
    )
