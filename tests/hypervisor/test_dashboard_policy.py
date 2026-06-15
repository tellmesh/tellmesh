"""Dashboard policy gates mutations through explicit approval."""

from __future__ import annotations

from hypervisor_dashboard_agent.policy import decision_for_uri, preview_action


def test_dashboard_blocks_repair_apply_without_approval():
    decision = decision_for_uri("repair://agent/demo.local/apply", policy="dev")
    assert decision.allowed is False
    assert decision.requires_approval is True


def test_dashboard_allows_repair_apply_with_approval():
    decision = decision_for_uri(
        "repair://agent/demo.local/apply",
        approved=True,
        policy="dev",
    )
    assert decision.allowed is True


def test_dashboard_blocks_browser_mutation_without_approval():
    decision = decision_for_uri("browser://chrome/page/open", policy="dev")
    assert decision.allowed is False
    assert decision.requires_approval is True


def test_dashboard_preview_marks_repair_apply_as_requires_approval():
    preview = preview_action("repair://agent/x/apply", policy="dev")
    assert preview["requires_approval"] is True
    assert preview["execute_allowed_with_approval"] is True
