"""Tests for markpact deploy blocks in deployments/README.md."""

from __future__ import annotations

from pathlib import Path

import yaml
from uri2pact import extract_markpact_blocks


def test_deployments_readme_has_markpact_deploy_blocks(repo_root: Path):
    readme = repo_root / "deployments" / "README.md"
    assert readme.is_file()
    blocks = extract_markpact_blocks(readme.read_text(encoding="utf-8"), "deploy")
    ids = []
    for block in blocks:
        data = yaml.safe_load(block["body"])
        ids.append(data["deployment"]["id"])
    assert "weather-map-agent.local" in ids
    assert "invoices-agent.local" in ids
    assert "hypervisor-dashboard.local" in ids
