from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hypervisor.routing.policy import PolicyRequest, evaluate_route_policy


@dataclass
class ApprovalDecision:
    allowed: bool
    reason: str | None
    force_dry_run: bool
    requires_approval: bool


def decision_for_uri(
    uri: str,
    *,
    approved: bool = False,
    dry_run: bool = False,
    readonly: bool = False,
    policy: str = "dev",
) -> ApprovalDecision:
    evaluation = evaluate_route_policy(
        uri,
        request=PolicyRequest(
            approved=approved,
            dry_run=dry_run,
            readonly=readonly,
            policy=policy,
            strict_approve=True,
        ),
    )
    return ApprovalDecision(
        allowed=evaluation.allowed,
        reason=evaluation.reason,
        force_dry_run=evaluation.force_dry_run,
        requires_approval=evaluation.requires_approval,
    )


def preview_action(uri: str, *, policy: str = "dev") -> dict[str, Any]:
    read_decision = decision_for_uri(uri, readonly=False, policy=policy)
    approve_decision = decision_for_uri(uri, approved=True, policy=policy)
    return {
        "uri": uri,
        "readonly_allowed": read_decision.allowed and not read_decision.force_dry_run,
        "dry_run_allowed": decision_for_uri(uri, dry_run=True, policy=policy).allowed,
        "execute_allowed_with_approval": approve_decision.allowed,
        "requires_approval": approve_decision.requires_approval or not read_decision.allowed,
        "policy": policy,
        "reason": read_decision.reason,
    }
