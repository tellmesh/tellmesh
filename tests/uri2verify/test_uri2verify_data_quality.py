"""Tests for uri2verify data quality layer."""

from __future__ import annotations

from pathlib import Path

import yaml

from touri.executor import call_uri
from uri2verify.result_checks import enrich_result_dict, technical_vs_business_ok


def _write_capability(tmp_path: Path, manifest: dict) -> Path:
    path = tmp_path / "demo.uri.capability.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return tmp_path


def test_data_quality_sets_verification_statuses(tmp_path: Path):
    manifest = {
        "version": 1,
        "capability": {
            "id": "demo.low_confidence",
            "scheme": "demo",
            "uri_template": "demo://check/{name}",
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
    }
    registry = _write_capability(tmp_path, manifest)
    result = call_uri("demo://check/item", registry)
    payload = enrich_result_dict(result.to_dict())
    assert payload["ok"] is False
    assert payload["data_quality_status"] == "failed"
    assert payload["verification_status"] == "failed"
    assert payload["errors"][0]["code"] == "PRICE_RESULT_NOT_RELEVANT"
    assert payload["errors"][0]["source"] == "uri2verify.data_quality"
    split = technical_vs_business_ok(payload)
    assert split["execution_ok"] is True
    assert split["service_ok"] is False
    assert split["business_ok"] is False
