"""Tests for uri2verify result status helpers."""

from __future__ import annotations

from uri3.results import service_result
from uri2verify.result_checks import apply_verification_statuses, technical_vs_business_ok


def test_technical_vs_business_split():
    payload = {
        "ok": False,
        "workflow_status": "completed",
        "execution_status": "completed",
        "service_result_status": "failed",
        "verification_status": "failed",
    }
    split = technical_vs_business_ok(payload)
    assert split["execution_ok"] is True
    assert split["service_ok"] is False
    assert split["business_ok"] is False


def test_apply_verification_statuses_on_success():
    result = service_result(ok=True, result_type="data", data={"x": 1})
    apply_verification_statuses(result, data_quality_checked=True)
    assert result.meta["data_quality_status"] == "passed"
    assert result.meta["verification_status"] == "passed"
