"""Tests for uri2verify capability verification plans."""

from __future__ import annotations

from pathlib import Path

from hypervisor.contract_registry.loader import load_contract_registry
from uri2verify.capability_tests import capability_test_plan_from_registry


def test_capability_test_plan_from_contract_registry(repo_root: Path):
    registry = load_contract_registry(repo_root)
    plan = capability_test_plan_from_registry(registry)
    assert plan
    kinds = {item["kind"] for item in plan}
    assert "resource_read" in kinds or "command" in kinds
