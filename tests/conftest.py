from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

import pytest

CLI_MODULES: dict[str, str] = {
    "uri3": "uri3.cli",
    "touri": "touri.cli",
    "hypervisor": "hypervisor.cli",
    "urigen": "urigen.cli",
    "urish": "urish.cli",
    "uri2flow": "uri2flow.cli",
    "uri2ops": "uri2ops.cli",
    "uri2run": "uri2run.cli",
    "uri2verify": "uri2verify.cli",
    "nl2uri": "nl2uri.cli",
    "nl2a": "nl2a.cli",
}


@pytest.fixture(scope="session")
def repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").is_file() and (parent / "examples").is_dir():
            return parent
    raise RuntimeError("hypervisor repo root not found")


@pytest.fixture(scope="session")
def www_root(repo_root: Path) -> Path:
    sys.path.insert(0, str(repo_root.parent.parent / "tellmesh" / "resource-agent-hypervisor"))
    from hypervisor.paths import resolve_www_dir

    resolved = resolve_www_dir(repo_root)
    if resolved is None or not (resolved / "index.html").is_file():
        pytest.skip("tellmesh/www checkout required (set HYPERVISOR_WWW_DIR)")
    return resolved


@pytest.fixture(scope="session", autouse=True)
def _hypervisor_repo_root_env(repo_root: Path):
    previous = os.environ.get("HYPERVISOR_REPO_ROOT")
    os.environ["HYPERVISOR_REPO_ROOT"] = str(repo_root.resolve())
    yield
    if previous is None:
        os.environ.pop("HYPERVISOR_REPO_ROOT", None)
    else:
        os.environ["HYPERVISOR_REPO_ROOT"] = previous


def workspace_pythonpath(repo_root: Path) -> str:
    tellmesh_root = repo_root.parent.parent / "tellmesh"
    paths = [
        repo_root,
        tellmesh_root / "uri3",
        tellmesh_root / "nl2uri",
        tellmesh_root / "uri2flow",
        tellmesh_root / "uri2ops",
        tellmesh_root / "touri",
        tellmesh_root / "uri2voice",
        tellmesh_root / "uri2pact",
        tellmesh_root / "uri2run",
        tellmesh_root / "uri2verify",
        tellmesh_root / "urigen",
        tellmesh_root / "urish",
        tellmesh_root / "resource-agent-hypervisor",
        tellmesh_root / "resource-agent-factory",
        tellmesh_root / "hypervisor-dashboard",
        repo_root / "examples" / "21_touri_voice",
    ]
    prefix = os.pathsep.join(str(path) for path in paths if path.is_dir())
    existing = os.environ.get("PYTHONPATH", "")
    return f"{prefix}{os.pathsep}{existing}" if existing else prefix


def workspace_env(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = workspace_pythonpath(repo_root)
    env["HYPERVISOR_REPO_ROOT"] = str(repo_root.resolve())
    env.setdefault("LANG", "en_US.UTF-8")
    env.setdefault("LC_ALL", env["LANG"])
    bin_dirs = [Path(sys.executable).resolve().parent, repo_root / ".venv" / "bin"]
    prepend = os.pathsep.join(str(path) for path in bin_dirs if path.is_dir())
    if prepend:
        env["PATH"] = f"{prepend}{os.pathsep}{env.get('PATH', '')}"
    return env


def cli_argv(
    name: str,
    *args: str,
    env: dict[str, str] | None = None,
    repo_root: Path | None = None,
) -> list[str]:
    """Resolve a workspace console script for subprocess use."""
    candidates: list[Path] = []
    exe_parent = Path(sys.executable).parent
    if exe_parent.name == "bin":
        candidates.append(exe_parent / name)
    if repo_root is not None:
        candidates.append(repo_root / ".venv" / "bin" / name)
    search_path = (env or os.environ).get("PATH", "")
    for directory in search_path.split(os.pathsep):
        if directory:
            candidates.append(Path(directory) / name)
    for script in candidates:
        if script.is_file():
            return [str(script), *args]
    found = shutil.which(name, path=search_path or None)
    if found:
        return [found, *args]
    module = CLI_MODULES.get(name)
    if module:
        code = (
            "from __future__ import annotations; "
            "import importlib, inspect, sys; "
            f"main = getattr(importlib.import_module({module!r}), 'main'); "
            "result = main(sys.argv[1:]) if inspect.signature(main).parameters else main(); "
            "raise SystemExit(0 if result is None else result)"
        )
        return [sys.executable, "-c", code, *args]
    return [name, *args]


@pytest.fixture(scope="session")
def examples_env(repo_root: Path) -> dict[str, str]:
    return workspace_env(repo_root)
