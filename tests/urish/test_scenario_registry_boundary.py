from __future__ import annotations

from urish.intent import detect_intent
from urish.scenario_registry import load_scenario_registries


def test_office_scenarios_are_loaded_from_domains_registry():
    registries = load_scenario_registries()
    sources = {registry["metadata"]["source"] for registry in registries}
    assert "domains/office/scenario_registry.yaml" in sources

    intent = detect_intent("połącz WooCommerce, BaseLinker i ERP; pokaż błędy w chacie")
    assert intent["kind"] == "office"
    assert intent["registry_source"] == "domains/office/scenario_registry.yaml"
    assert "contracts/agents/invoices_agent.yaml" in intent["artifacts"]["contracts"]


def test_urish_has_no_office_specific_compat_modules(repo_root):
    assert not (repo_root / "packages/urish/urish/office_intent.py").exists()
    assert not (repo_root / "packages/urish/urish/office_scenarios.py").exists()
