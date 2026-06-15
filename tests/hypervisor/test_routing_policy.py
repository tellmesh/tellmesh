from __future__ import annotations

from pathlib import Path

from hypervisor.routing.policy import PolicyRequest, evaluate_route_policy


def test_strict_approve_blocks_browser_without_approval():
    evaluation = evaluate_route_policy(
        "browser://chrome/page/open",
        request=PolicyRequest(strict_approve=True, policy="dev"),
    )

    assert evaluation.allowed is False
    assert evaluation.requires_approval is True


def test_resolver_allows_browser_with_approval(repo_root: Path):
    evaluation = evaluate_route_policy(
        "browser://chrome/page/open",
        request=PolicyRequest(approved=True, policy="dev"),
        root=repo_root,
    )

    assert evaluation.allowed is True
    assert evaluation.requires_approval is False


def test_strict_approve_blocks_shell_mutation_without_approval():
    evaluation = evaluate_route_policy(
        "shell://echo",
        request=PolicyRequest(policy="dev", strict_approve=True),
    )

    assert evaluation.allowed is False
    assert evaluation.requires_approval is True


def test_health_read_allowed_without_approval():
    evaluation = evaluate_route_policy(
        "health://agent/demo.local",
        request=PolicyRequest(strict_approve=True, policy="dev"),
    )

    assert evaluation.allowed is True
    assert evaluation.requires_approval is False
