"""Inline example scenarios (no run.sh or lightweight checks)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.conftest import cli_argv
from tests.examples.conftest import docker_available, run_shell


def _local_agent_url(repo_root: Path, env: dict) -> str | None:
    for port in range(8101, 8131):
        url = f"http://localhost:{port}/health"
        probe = run_shell(
            repo_root,
            ["curl", "-sf", "--max-time", "2", url],
            env=env,
            timeout_s=10,
        )
        if probe.returncode == 0:
            return url.removesuffix("/health")
    return None


@pytest.mark.examples
def test_example_02_uri3_scan_http(repo_root: Path, examples_env):
    agent_url = _local_agent_url(repo_root, examples_env)
    if agent_url is None:
        pytest.skip("no local HTTP agent on ports 8101-8130")
    result = run_shell(
        repo_root,
        cli_argv(
            "uri3",
            "scan",
            agent_url,
            env=examples_env,
            repo_root=repo_root,
        ),
        env=examples_env,
        timeout_s=60,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.examples
@pytest.mark.docker
def test_example_03_ssh_docker_testenv(repo_root: Path, examples_env):
    if not docker_available():
        pytest.skip("docker not available")
    up = run_shell(repo_root, ["make", "docker-testenv-up"], env=examples_env, timeout_s=240)
    assert up.returncode == 0, up.stderr
    try:
        env = {
            **examples_env,
            "HYPERVISOR_SSH_PASSWORD": examples_env.get(
                "HYPERVISOR_SSH_PASSWORD",
                "deploy",
            ),
        }
        scan = run_shell(
            repo_root,
            cli_argv("uri3", "scan", "ssh", env=env, repo_root=repo_root),
            env=env,
            timeout_s=120,
        )
        assert scan.returncode == 0, scan.stderr
    finally:
        down = run_shell(
            repo_root,
            ["make", "docker-testenv-down"],
            env=examples_env,
            timeout_s=120,
        )
        assert down.returncode == 0, down.stderr


@pytest.mark.examples
def test_example_05_meta_repair(repo_root: Path, examples_env):
    result = run_shell(
        repo_root,
        [
            "python",
            "-m",
            "meta_agent.cli",
            "repair",
            "examples/05_meta_repair/broken_agent.yaml",
        ],
        env=examples_env,
    )
    assert result.returncode == 0
    assert "changed: true" in result.stdout


@pytest.mark.examples
def test_example_06_orders_agent(repo_root: Path, examples_env):
    result = run_shell(
        repo_root,
        ["python", "-m", "generator.validate", "examples/06_orders_agent"],
        env=examples_env,
    )
    assert result.returncode == 0
    assert "Validated 1" in result.stdout


@pytest.mark.examples
def test_example_07_invoices_agent(repo_root: Path, examples_env):
    prompt = (repo_root / "examples/07_invoices_agent/create_invoices_agent_prompt.txt").read_text(
        encoding="utf-8"
    )
    result = run_shell(
        repo_root,
        ["python", "-m", "meta_agent.cli", "plan", prompt.strip()],
        env=examples_env,
        timeout_s=120,
    )
    assert result.returncode == 0
    assert "contracts/agents" in result.stdout


@pytest.mark.examples
def test_example_08_evolution(repo_root: Path, examples_env):
    result = run_shell(repo_root, ["make", "evolution-check"], env=examples_env)
    assert result.returncode == 0


@pytest.mark.examples
def test_example_15_playwright_mock_via_uri3(repo_root: Path, examples_env):
    graph = repo_root / "examples/14_workflow_executor_mock/task_graph.yaml"
    validate = run_shell(
        repo_root,
        cli_argv("uri3", "validate-workflow", str(graph), env=examples_env, repo_root=repo_root),
        env=examples_env,
    )
    assert validate.returncode == 0
    run = run_shell(
        repo_root,
        cli_argv(
            "uri3",
            "run-workflow",
            str(graph),
            "--approve",
            "--browser",
            "mock",
            env=examples_env,
            repo_root=repo_root,
        ),
        env=examples_env,
        timeout_s=120,
    )
    assert run.returncode == 0


@pytest.mark.examples
def test_example_16www_landing_monitor(repo_root: Path, examples_env):
    from tests.examples.conftest import www_available

    graph = repo_root / "examples/16_www_landing_monitor/task_graph.yaml"
    validate = run_shell(
        repo_root,
        cli_argv("uri3", "validate-workflow", str(graph), env=examples_env, repo_root=repo_root),
        env=examples_env,
    )
    assert validate.returncode == 0
    if not www_available():
        pytest.skip("WWW not running on localhost:8788")
    dry = run_shell(
        repo_root,
        cli_argv(
            "uri3",
            "run-workflow",
            str(graph),
            "--dry-run",
            env=examples_env,
            repo_root=repo_root,
        ),
        env=examples_env,
    )
    assert dry.returncode == 0


@pytest.mark.examples
def test_example_22_dashboard_agent(repo_root: Path, examples_env):
    manifest = repo_root / "examples/22_dashboard_agent/process_view.uri.capability.yaml"
    validate = run_shell(
        repo_root,
        cli_argv("touri", "validate", str(manifest), env=examples_env, repo_root=repo_root),
        env=examples_env,
    )
    assert validate.returncode == 0
    listing = run_shell(
        repo_root,
        cli_argv(
            "touri",
            "list",
            "examples/22_dashboard_agent",
            env=examples_env,
            repo_root=repo_root,
        ),
        env=examples_env,
    )
    assert listing.returncode == 0
