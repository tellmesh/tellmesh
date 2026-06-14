"""Tests for touri fallback backends."""

from __future__ import annotations

from pathlib import Path

import yaml

from touri.executor import call_uri


def test_fallback_applies_mock_after_data_quality_failure(tmp_path: Path):
    manifest = {
        "version": 1,
        "capability": {
            "id": "demo.fallback",
            "scheme": "demo",
            "uri_template": "demo://fallback/{name}",
            "operation": "read",
            "kind": "query",
        },
        "backend": {
            "type": "python",
            "target": "python://touri_examples.validators:low_confidence_backend",
        },
        "data_quality": {
            "failure_code": "PRICE_RESULT_NOT_RELEVANT",
            "validators": ["python://touri_examples.validators:reject_low_confidence"],
        },
        "fallbacks": [
            {
                "when": "PRICE_RESULT_NOT_RELEVANT",
                "backend": {"type": "mock"},
            }
        ],
    }
    path = tmp_path / "demo.uri.capability.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    result = call_uri("demo://fallback/item", tmp_path)
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["service_result_status"] == "succeeded"
    assert payload["backend"] == "mock"
    assert any("fallback applied" in warning for warning in payload.get("warnings", []))
