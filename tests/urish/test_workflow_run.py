"""Tests for urish workflow run backend."""

from __future__ import annotations

from urish.backends.run import run_target


def test_run_workflow_uri_dry_run():
    result = run_target("workflow://order/woocommerce-to-erp/dry-run", dry_run=True)
    assert result.get("ok") is True
    assert result.get("result_type") in {"plan", "workflow", "query"}


def test_explain_workflow_order_resolves_touri():
    from urish.backends.explain import explain_target

    payload = explain_target("workflow://order/woocommerce-to-erp")
    assert payload.get("matched_registry") == "touri"
    assert payload.get("capability") == "workflow.order.woocommerce_to_erp"


def test_run_workflow_supplier_report():
    result = run_target("workflow://office/supplier-report/monthly", dry_run=True)
    assert result.get("ok") is True


def test_run_workflow_portal_zus_dry_run():
    result = run_target("workflow://portal/zus-form/dry-run", dry_run=True)
    assert result.get("ok") is True


def test_run_workflow_bank_batch_dry_run():
    result = run_target("workflow://bank/batch-transfer/dry-run", dry_run=True)
    assert result.get("ok") is True


def test_explain_cron_uri_resolves_touri():
    from urish.backends.explain import explain_target

    payload = explain_target("cron://www/monitor/landing")
    assert payload.get("matched_registry") == "touri"
    assert payload.get("capability") == "cron.www.landing_monitor"


def test_run_cron_www_monitor_dry_run():
    result = run_target("cron://www/monitor/landing", dry_run=True)
    assert result.get("ok") is True


def test_call_health_agent_system_uri():
    from urish.backends.call import call_uri
    from urish.policy import PolicyOptions

    result = call_uri(
        "health://agent/invoices-agent.local",
        {},
        policy_options=PolicyOptions.from_flags(dry_run=False),
    )
    assert result.get("result_type") in {"health", "system_uri"}
    assert "agent_id" in (result.get("data") or {})
