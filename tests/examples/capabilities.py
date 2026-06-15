"""Probe host capabilities for real-mode example commands."""

from __future__ import annotations

import json
import platform
import shutil
import socket
import subprocess
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from tests.conftest import workspace_env
from tests.examples.conftest import docker_available, playwright_available


def _tcp_open(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _http_ok(url: str, timeout: float = 3.0) -> bool:
    curl = shutil.which("curl")
    if curl is None:
        return False
    probe = subprocess.run(
        [curl, "-sf", "--max-time", str(int(timeout)), url],
        capture_output=True,
        timeout=timeout + 2,
        check=False,
    )
    return probe.returncode == 0


def _adb_device() -> bool:
    adb = shutil.which("adb")
    if adb is None:
        return False
    probe = subprocess.run(
        [adb, "devices"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if probe.returncode != 0:
        return False
    lines = [line for line in probe.stdout.splitlines()[1:] if line.strip()]
    return any("\tdevice" in line for line in lines)


def _uia_available() -> bool:
    if platform.system().lower() != "windows":
        return False
    try:
        import pywinauto  # noqa: F401

        return True
    except ImportError:
        return False


def _cli_available(name: str, repo_root: Path) -> bool:
    env = workspace_env(repo_root)
    path = env.get("PATH", "")
    if shutil.which(name, path=path):
        return True
    module_map = {
        "uri": "urish.cli",
        "uri3": "uri3.cli",
        "hypervisor": "hypervisor.cli",
        "touri": "touri.cli",
        "uri2ops": "uri2ops.cli",
        "uri2flow": "uri2flow.cli",
        "nl2uri": "nl2uri.cli",
    }
    mod = module_map.get(name)
    if mod is None:
        return False
    python = shutil.which("python", path=path) or shutil.which("python3", path=path)
    if python is None:
        return False
    probe = subprocess.run(
        [python, "-m", mod, "--help"],
        env=env,
        capture_output=True,
        timeout=30,
        check=False,
    )
    return probe.returncode == 0


def _weather_agent_health() -> bool:
    for port in range(8101, 8131):
        if _http_ok(f"http://localhost:{port}/health"):
            curl = shutil.which("curl")
            if curl is None:
                continue
            probe = subprocess.run(
                [curl, "-sf", "--max-time", "2", f"http://localhost:{port}/health"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            if probe.returncode == 0 and "weather-map" in probe.stdout:
                return True
    return False


@dataclass
class CapabilityProbe:
    id: str
    label: str
    available: bool
    detail: str = ""


@dataclass
class MachineCapabilities:
    probes: list[CapabilityProbe] = field(default_factory=list)

    def available(self, requirement: str) -> bool:
        for probe in self.probes:
            if probe.id == requirement:
                return probe.available
        return False

    def to_dict(self) -> dict:
        return {
            "probes": [asdict(p) for p in self.probes],
            "available": [p.id for p in self.probes if p.available],
            "unavailable": [p.id for p in self.probes if not p.available],
        }


def probe_machine(repo_root: Path) -> MachineCapabilities:
    """Return which real-mode requirements are satisfied on this host."""
    env = workspace_env(repo_root)
    checks: list[tuple[str, str, Callable[[], bool], str]] = [
        ("cli_uri", "uri / urish CLI", lambda: _cli_available("uri", repo_root), ""),
        ("cli_uri3", "uri3 CLI", lambda: _cli_available("uri3", repo_root), ""),
        ("cli_hypervisor", "hypervisor CLI", lambda: _cli_available("hypervisor", repo_root), ""),
        ("cli_touri", "touri CLI", lambda: _cli_available("touri", repo_root), ""),
        ("cli_uri2flow", "uri2flow CLI", lambda: _cli_available("uri2flow", repo_root), ""),
        ("cli_nl2uri", "nl2uri CLI", lambda: _cli_available("nl2uri", repo_root), ""),
        ("docker", "Docker daemon", docker_available, ""),
        (
            "playwright",
            "Playwright + Chromium",
            lambda: playwright_available(repo_root),
            "pip install -e '.[browser]' && playwright install chromium",
        ),
        (
            "agent_http_8101",
            "HTTP agent on :8101",
            lambda: _http_ok("http://localhost:8101/health"),
            "hypervisor run-agent weather-map-agent.local --detach --wait-healthy",
        ),
        (
            "agent_http_any",
            "Any local HTTP agent (8101–8130)",
            lambda: any(
                _http_ok(f"http://localhost:{port}/health") for port in range(8101, 8131)
            ),
            "",
        ),
        (
            "weather_agent",
            "weather-map-agent HTTP health",
            _weather_agent_health,
            "hypervisor run-agent weather-map-agent.local --detach --wait-healthy",
        ),
        (
            "www_8788",
            "Taskinity WWW on :8788",
            lambda: _http_ok("http://localhost:8788/www/"),
            "make start",
        ),
        (
            "openrouter",
            "OPENROUTER_API_KEY set",
            lambda: bool(env.get("OPENROUTER_API_KEY", "").strip()),
            "export OPENROUTER_API_KEY=…",
        ),
        ("adb", "ADB device connected", _adb_device, "adb devices"),
        ("uia", "Windows UIA (pywinauto)", _uia_available, "Windows + pip install pywinauto"),
        (
            "curl",
            "curl available",
            lambda: shutil.which("curl") is not None,
            "",
        ),
    ]

    probes: list[CapabilityProbe] = []
    for req_id, label, fn, hint in checks:
        try:
            ok = fn()
        except Exception as exc:  # noqa: BLE001
            ok = False
            detail = f"probe error: {exc}"
        else:
            detail = "" if ok else hint
        probes.append(CapabilityProbe(id=req_id, label=label, available=ok, detail=detail))

    return MachineCapabilities(probes=probes)


def write_capabilities_report(repo_root: Path, caps: MachineCapabilities, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(caps.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
