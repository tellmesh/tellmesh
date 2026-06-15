"""Tests for markpact scenario loaders."""

from __future__ import annotations

from pathlib import Path

from uri2pact.scenarios import (
    load_markpact_scenario_dicts,
    load_markpact_scenario_registry_dicts,
)


def test_load_office_markpact_scenarios(repo_root: Path):
    ref = f"markpact://{repo_root / 'domains' / 'office' / 'README.md'}"
    scenarios = load_markpact_scenario_dicts(ref, root=repo_root)
    ids = {item["id"] for item in scenarios}
    assert ids == {
        "website_report",
        "portal_zus_form",
        "erp_subiekt",
        "invoice_batch_woo",
        "bank_batch",
        "android_2fa",
    }


def test_load_office_markpact_scenario_registry_includes_yaml(repo_root: Path):
    ref = f"markpact://{repo_root / 'domains' / 'office' / 'README.md'}"
    registries = load_markpact_scenario_registry_dicts(ref, root=repo_root)
    assert len(registries) == 1
    registry = registries[0]
    assert registry["kind"] == "urish.scenario_registry"
    assert registry["intent_kind"] == "office"
    assert len(registry.get("scenarios") or []) == 6
