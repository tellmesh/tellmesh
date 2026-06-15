"""Run all catalog examples from a single entry point (shared with pytest)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.conftest import cli_argv, workspace_env  # noqa: E402
from tests.examples.catalog import ALL_EXAMPLES, ExampleSpec  # noqa: E402
from tests.examples.conftest import (  # noqa: E402
    docker_available,
    playwright_available,
    playwright_python,
    run_shell,
    www_available,
)

SKIP_EXIT = 77

RunFn = Callable[[Path, dict[str, str]], int]


def _skip(_root: Path, _env: dict[str, str]) -> int:
    return SKIP_EXIT


def _run_sh(spec: ExampleSpec, root: Path, env: dict[str, str]) -> int:
    result = run_shell(root, ["bash", str(root / spec.path)], env=env, timeout_s=spec.timeout_s)
    return result.returncode


def _local_agent_url(root: Path, env: dict[str, str]) -> str | None:
    for port in range(8101, 8131):
        url = f"http://localhost:{port}/health"
        probe = run_shell(
            root,
            ["curl", "-sf", "--max-time", "2", url],
            env=env,
            timeout_s=10,
        )
        if probe.returncode == 0:
            return url.removesuffix("/health")
    return None


def _ex02(root: Path, env: dict[str, str]) -> int:
    agent_url = _local_agent_url(root, env)
    if agent_url is None:
        return SKIP_EXIT
    result = run_shell(
        root,
        cli_argv("uri3", "scan", agent_url, env=env, repo_root=root),
        env=env,
        timeout_s=60,
    )
    return result.returncode


def _ex03(root: Path, env: dict[str, str]) -> int:
    if not docker_available():
        return SKIP_EXIT
    up = run_shell(root, ["make", "docker-testenv-up"], env=env, timeout_s=240)
    if up.returncode != 0:
        return up.returncode
    try:
        merged = {**env, "HYPERVISOR_SSH_PASSWORD": env.get("HYPERVISOR_SSH_PASSWORD", "deploy")}
        scan = run_shell(
            root,
            cli_argv("uri3", "scan", "ssh", env=merged, repo_root=root),
            env=merged,
            timeout_s=120,
        )
        return scan.returncode
    finally:
        run_shell(root, ["make", "docker-testenv-down"], env=env, timeout_s=120)


def _ex05(root: Path, env: dict[str, str]) -> int:
    result = run_shell(
        root,
        ["python", "-m", "meta_agent.cli", "repair", "examples/05_meta_repair/broken_agent.yaml"],
        env=env,
    )
    if result.returncode != 0:
        return result.returncode
    return 0 if "changed: true" in result.stdout else 1


def _ex06(root: Path, env: dict[str, str]) -> int:
    result = run_shell(
        root,
        ["python", "-m", "generator.validate", "examples/06_orders_agent"],
        env=env,
    )
    if result.returncode != 0:
        return result.returncode
    return 0 if "Validated 1" in result.stdout else 1


def _ex07(root: Path, env: dict[str, str]) -> int:
    prompt = (
        root / "examples/07_invoices_agent/create_invoices_agent_prompt.txt"
    ).read_text(encoding="utf-8")
    result = run_shell(
        root,
        ["python", "-m", "meta_agent.cli", "plan", prompt.strip()],
        env=env,
        timeout_s=120,
    )
    if result.returncode != 0:
        return result.returncode
    return 0 if "contracts/agents" in result.stdout else 1


def _ex08(root: Path, env: dict[str, str]) -> int:
    return run_shell(root, ["make", "evolution-check"], env=env).returncode


def _ex15pw(root: Path, env: dict[str, str]) -> int:
    graph = root / "examples/14_workflow_executor_mock/task_graph.yaml"
    validate = run_shell(
        root,
        cli_argv("uri3", "validate-workflow", str(graph), env=env, repo_root=root),
        env=env,
    )
    if validate.returncode != 0:
        return validate.returncode
    run = run_shell(
        root,
        cli_argv(
            "uri3",
            "run-workflow",
            str(graph),
            "--approve",
            "--browser",
            "mock",
            env=env,
            repo_root=root,
        ),
        env=env,
        timeout_s=120,
    )
    return run.returncode


def _ex16www(root: Path, env: dict[str, str]) -> int:
    graph = root / "examples/16_www_landing_monitor/task_graph.yaml"
    validate = run_shell(
        root,
        cli_argv("uri3", "validate-workflow", str(graph), env=env, repo_root=root),
        env=env,
    )
    if validate.returncode != 0:
        return validate.returncode
    if not www_available():
        return SKIP_EXIT
    dry = run_shell(
        root,
        cli_argv("uri3", "run-workflow", str(graph), "--dry-run", env=env, repo_root=root),
        env=env,
    )
    if dry.returncode != 0:
        return dry.returncode
    monitor = run_shell(
        root,
        ["python3", "scripts/www/monitor_landing.py", "--url", "http://localhost:8788/www/"],
        env=env,
        timeout_s=120,
    )
    return monitor.returncode


def _ex22dash(root: Path, env: dict[str, str]) -> int:
    manifest = root / "examples/22_dashboard_agent/process_view.uri.capability.yaml"
    validate = run_shell(
        root,
        cli_argv("touri", "validate", str(manifest), env=env, repo_root=root),
        env=env,
    )
    if validate.returncode != 0:
        return validate.returncode
    listing = run_shell(
        root,
        cli_argv("touri", "list", "examples/22_dashboard_agent", env=env, repo_root=root),
        env=env,
    )
    return listing.returncode


def _ex11(root: Path, env: dict[str, str]) -> int:
    if not playwright_available(root):
        return SKIP_EXIT
    return run_shell(
        root,
        ["bash", "examples/11_playwright_browser/run.sh"],
        env=env,
        timeout_s=180,
    ).returncode


INLINE_RUNNERS: dict[str, RunFn] = {
    "02": _ex02,
    "03": _ex03,
    "05": _ex05,
    "06": _ex06,
    "07": _ex07,
    "08": _ex08,
    "11": _ex11,
    "15pw": _ex15pw,
    "16www": _ex16www,
    "22dash": _ex22dash,
}

# Shell runner order (matches legacy scripts/test-all-examples.sh).
SHELL_RUN_ORDER: tuple[str, ...] = (
    "01",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "12",
    "13op",
    "13nl",
    "14wf",
    "14srv",
    "15cf",
    "15pw",
    "16",
    "17",
    "18",
    "20",
    "21",
    "22",
    "23",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "16www",
    "22dash",
    "11",
    "02",
    "03",
)

_CATALOG_BY_ID = {spec.id: spec for spec in ALL_EXAMPLES}


def _should_skip(spec: ExampleSpec, root: Path) -> str | None:
    if "docker" in spec.markers and not docker_available():
        return "docker not available"
    if "playwright" in spec.markers and not playwright_available(root):
        return "playwright not installed"
    if "www" in spec.markers and not www_available():
        return "WWW not running on localhost:8788"
    return None


def run_example(spec: ExampleSpec, *, root: Path, env: dict[str, str]) -> int:
    reason = _should_skip(spec, root)
    if reason:
        print(f"⊘ SKIP: {spec.id} {spec.name} ({reason})")
        return SKIP_EXIT
    if spec.kind == "run_sh":
        return _run_sh(spec, root, env)
    runner = INLINE_RUNNERS.get(spec.id)
    if runner is None:
        print(f"✗ FAIL: {spec.id} {spec.name} (no inline runner registered)")
        return 1
    return runner(root, env)


def run_catalog(*, root: Path | None = None, order: tuple[str, ...] = SHELL_RUN_ORDER) -> int:
    repo = root or Path(__file__).resolve().parents[2]
    env = {**workspace_env(repo), "PYTHON": playwright_python(repo) or "python3"}
    pass_count = fail_count = skip_count = 0
    results: list[str] = []

    print("Hypervisor examples test run")
    print(f"Root: {repo}")
    print(f"Catalog: {len(ALL_EXAMPLES)} examples")

    for example_id in order:
        spec = _CATALOG_BY_ID.get(example_id)
        if spec is None:
            print(f"✗ FAIL: missing catalog entry for {example_id}")
            fail_count += 1
            results.append(f"FAIL  {example_id}  (missing from catalog)")
            continue
        print("")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"▶ Example {spec.id}: {spec.name}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        code = run_example(spec, root=repo, env=env)
        if code == 0:
            pass_count += 1
            results.append(f"PASS  {spec.id}  {spec.name}")
            print(f"✓ PASS: {spec.id} {spec.name}")
        elif code == SKIP_EXIT:
            skip_count += 1
            results.append(f"SKIP  {spec.id}  {spec.name}")
            print(f"⊘ SKIP: {spec.id} {spec.name}")
        else:
            fail_count += 1
            results.append(f"FAIL  {spec.id}  {spec.name}")
            print(f"✗ FAIL: {spec.id} {spec.name} (exit {code})")

    print("")
    print("══════════════════════════════════════════════════")
    print("SUMMARY")
    print("══════════════════════════════════════════════════")
    for row in results:
        print(row)
    print("")
    total = pass_count + fail_count + skip_count
    print(f"PASS={pass_count}  FAIL={fail_count}  SKIP={skip_count}  TOTAL={total}")
    return 1 if fail_count else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="Repository root")
    args = parser.parse_args(argv)
    return run_catalog(root=args.root)


if __name__ == "__main__":
    raise SystemExit(main())
