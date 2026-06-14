"""Tests for extended uri3 explain output."""

from __future__ import annotations

from pathlib import Path

import yaml

from uri3.resolvers.explain import explain_uri


def test_explain_includes_verification_hints(repo_root: Path):
    payload = explain_uri("weather://forecast/Gdansk/14/html", root=repo_root)
    verification = payload["verification"]
    assert verification["source"] == "uri2verify"
    assert verification["matched_registry"] == "touri"
    assert "expected_status_fields" in verification
    assert "data_quality_status" in verification["expected_status_fields"]


def test_explain_includes_fallbacks_and_data_quality(tmp_path: Path):
    manifest = {
        "version": 1,
        "capability": {
            "id": "demo.fallback",
            "scheme": "demo",
            "uri_template": "demo://fallback/{name}",
            "operation": "read",
            "kind": "query",
        },
        "backend": {"type": "python", "target": "python://touri_examples.validators:low_confidence_backend"},
        "data_quality": {
            "failure_code": "PRICE_RESULT_NOT_RELEVANT",
            "validators": ["python://touri_examples.validators:reject_low_confidence"],
        },
        "fallbacks": [{"when": "PRICE_RESULT_NOT_RELEVANT", "backend": {"type": "mock"}}],
    }
    path = tmp_path / "demo.uri.capability.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    payload = explain_uri("demo://fallback/item", registry_root=tmp_path)
    assert payload["verification"]["data_quality_enabled"] is True
    assert payload["verification"]["fallback_count"] == 1
    assert payload["fallbacks"][0]["backend_type"] == "mock"
    assert payload["verification"]["data_quality"]["failure_code"] == "PRICE_RESULT_NOT_RELEVANT"
