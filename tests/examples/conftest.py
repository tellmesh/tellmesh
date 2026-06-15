"""Fixtures for examples integration tests."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.conftest import workspace_env


@pytest.fixture(scope="session")
def repo_root() -> Path:
    root = Path(__file__).resolve().parents[2]
    assert (root / "pyproject.toml").is_file()
    assert (root / "examples").is_dir()
    return root


@pytest.fixture(scope="session")
def examples_env(repo_root: Path) -> dict[str, str]:
    env = workspace_env(repo_root)
    pw = playwright_python(repo_root)
    env["PYTHON"] = pw or sys.executable
    return env


def run_shell(
    repo_root: Path,
    command: list[str],
    *,
    env: dict[str, str],
    timeout_s: int = 120,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout_s,
        check=False,
    )


def docker_available() -> bool:
    if shutil.which("docker") is None:
        return False
    probe = subprocess.run(["docker", "info"], capture_output=True, timeout=30, check=False)
    return probe.returncode == 0


def _python_candidates(repo_root: Path | None = None) -> tuple[list[str], dict[str, str] | None]:
    env = workspace_env(repo_root) if repo_root is not None else None
    paths = []
    if env is not None:
        paths.append(env.get("PATH", ""))
    paths.append("")

    candidates: list[str] = []

    def add(candidate: str | None) -> None:
        if candidate and candidate not in candidates:
            candidates.append(candidate)

    add(sys.executable)
    for path in paths:
        for name in ("python3", "python"):
            add(shutil.which(name, path=path) if path else shutil.which(name))
    return candidates, env


def _python_runs_playwright(python: str, env: dict[str, str] | None) -> bool:
    probe = subprocess.run(
        [
            python,
            "-c",
            (
                "from playwright.sync_api import sync_playwright\n"
                "with sync_playwright() as p:\n"
                "    browser = p.chromium.launch(headless=True)\n"
                "    browser.close()\n"
            ),
        ],
        env=env,
        capture_output=True,
        timeout=45,
        check=False,
    )
    return probe.returncode == 0


def playwright_python(repo_root: Path | None = None) -> str | None:
    candidates, env = _python_candidates(repo_root)
    for python in candidates:
        if _python_runs_playwright(python, env):
            return python
    return None


def playwright_available(repo_root: Path | None = None) -> bool:
    if repo_root is not None:
        return playwright_python(repo_root) is not None
    return playwright_python(None) is not None


def www_available() -> bool:
    curl = shutil.which("curl")
    if curl is None:
        return False
    probe = subprocess.run(
        [curl, "-sf", "--max-time", "3", "http://localhost:8788/www/"],
        capture_output=True,
        timeout=10,
        check=False,
    )
    return probe.returncode == 0


def skip_if_markers(spec, repo_root: Path) -> None:
    if "docker" in spec.markers and not docker_available():
        pytest.skip("docker not available")
    if "playwright" in spec.markers and not playwright_available(repo_root):
        pytest.skip(
            "playwright not installed "
            "(pip install -e '.[browser]' && playwright install chromium)"
        )
    if "www" in spec.markers and not www_available():
        pytest.skip("WWW not running on localhost:8788 (make start)")
