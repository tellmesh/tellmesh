"""All example commands: default (mock/dry-run) and optional real-mode variants."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from tests.examples.catalog import ALL_EXAMPLES, RUN_SH_EXAMPLES

Tier = Literal["mock", "dry-run", "real", "validate"]


@dataclass(frozen=True)
class CommandSpec:
    id: str
    example_id: str
    label: str
    argv: tuple[str, ...]
    tier: Tier
    requires: tuple[str, ...] = ()
    category: str = "general"
    timeout_s: int = 120
    shell: bool = False  # run via bash -lc


def _run_sh_commands() -> tuple[CommandSpec, ...]:
    out: list[CommandSpec] = []
    for spec in RUN_SH_EXAMPLES:
        tier: Tier = "mock"
        if spec.id in {"09", "13nl", "30", "32", "33"}:
            tier = "dry-run"
        if spec.id == "11":
            tier = "real"
        requires: tuple[str, ...] = ()
        if "playwright" in spec.markers:
            requires = ("playwright",)
        if spec.id == "23":
            requires = ("agent_http_any",)
        out.append(
            CommandSpec(
                id=f"ex{spec.id}-run_sh",
                example_id=spec.id,
                label=f"bash {spec.path}",
                argv=("bash", spec.path),
                tier=tier,
                requires=requires,
                category="run_sh",
                timeout_s=spec.timeout_s,
            )
        )
    return tuple(out)


DEFAULT_COMMANDS: tuple[CommandSpec, ...] = _run_sh_commands() + (
    CommandSpec(
        "ex02-scan",
        "02",
        "uri3 scan http://localhost:8101",
        ("uri3", "scan", "http://localhost:8101"),
        "real",
        ("agent_http_8101",),
        "scan",
    ),
    CommandSpec(
        "ex03-ssh",
        "03",
        "uri3 scan ssh (docker testenv)",
        ("uri3", "scan", "ssh"),
        "real",
        ("docker",),
        "scan",
        300,
    ),
    CommandSpec(
        "ex05-repair",
        "05",
        "meta_agent repair broken_agent.yaml",
        ("python", "-m", "meta_agent.cli", "repair", "examples/05_meta_repair/broken_agent.yaml"),
        "mock",
        category="meta",
    ),
    CommandSpec(
        "ex06-validate",
        "06",
        "generator.validate orders_agent",
        ("python", "-m", "generator.validate", "examples/06_orders_agent"),
        "validate",
        category="contract",
    ),
    CommandSpec(
        "ex07-plan",
        "07",
        "meta_agent plan invoices prompt",
        ("python", "-m", "meta_agent.cli", "plan", "__PROMPT__"),
        "mock",
        category="meta",
    ),
    CommandSpec(
        "ex08-evolution",
        "08",
        "make evolution-check",
        ("make", "evolution-check"),
        "validate",
        category="evolution",
    ),
    CommandSpec(
        "ex15pw-mock",
        "15pw",
        "uri3 run-workflow 14 mock browser",
        (
            "uri3",
            "run-workflow",
            "examples/14_workflow_executor_mock/task_graph.yaml",
            "--approve",
            "--browser",
            "mock",
        ),
        "mock",
        category="browser",
    ),
    CommandSpec(
        "ex16www-validate",
        "16www",
        "validate landing monitor workflow",
        ("uri3", "validate-workflow", "examples/16_www_landing_monitor/task_graph.yaml"),
        "validate",
        category="monitor",
    ),
    CommandSpec(
        "ex16www-dry-run",
        "16www",
        "dry-run landing monitor workflow",
        (
            "uri3",
            "run-workflow",
            "examples/16_www_landing_monitor/task_graph.yaml",
            "--dry-run",
        ),
        "dry-run",
        ("www_8788",),
        "monitor",
    ),
    CommandSpec(
        "ex22dash-validate",
        "22dash",
        "touri validate dashboard capabilities",
        (
            "touri",
            "validate",
            "examples/22_dashboard_agent/process_view.uri.capability.yaml",
        ),
        "validate",
        category="dashboard",
    ),
    CommandSpec(
        "ex22dash-list",
        "22dash",
        "touri list dashboard capabilities",
        ("touri", "list", "examples/22_dashboard_agent"),
        "validate",
        category="dashboard",
    ),
)

REAL_COMMANDS: tuple[CommandSpec, ...] = (
    CommandSpec(
        "ex02-scan-any",
        "02",
        "uri3 scan http (auto-discover)",
        ("uri3", "scan", "http"),
        "real",
        ("agent_http_any",),
        "scan",
    ),
    CommandSpec(
        "ex09-run-agent",
        "09",
        "hypervisor run-agent weather-map (real start)",
        (
            "hypervisor",
            "run-agent",
            "weather-map-agent.local",
            "--detach",
            "--wait-healthy",
        ),
        "real",
        (),
        "agent",
        180,
    ),
    CommandSpec(
        "ex10-playwright",
        "10",
        "uri2ops current weather health with playwright",
        ("python3", "scripts/examples/effective_weather_playwright.py", "--engine", "uri2ops"),
        "real",
        ("playwright", "weather_agent"),
        "browser",
        180,
    ),
    CommandSpec(
        "ex11-playwright",
        "11",
        "playwright in-process browser demo",
        ("bash", "examples/11_playwright_browser/run.sh"),
        "real",
        ("playwright",),
        "browser",
        180,
    ),
    CommandSpec(
        "ex12-adb",
        "12",
        "uri2ops android screenshot (real adb)",
        (
            "uri2ops",
            "run",
            "examples/12_android_operator/task.android.yaml",
            "--adapter",
            "adb",
            "--approve",
        ),
        "real",
        ("adb",),
        "android",
        120,
    ),
    CommandSpec(
        "ex13op-uia",
        "13op",
        "uri2ops pcwin focus (real UIA)",
        (
            "uri2ops",
            "run",
            "examples/13_pcwin_operator/task.pcwin.yaml",
            "--adapter",
            "uia",
            "--approve",
        ),
        "real",
        ("uia",),
        "desktop",
        120,
    ),
    CommandSpec(
        "ex15cf-run",
        "15cf",
        "uri3 run-flow compact weather graph (mock browser)",
        (
            "uri3",
            "run-flow",
            "examples/15_compact_uri_flow/weather.uri.flow.yaml",
            "--approve",
            "--browser",
            "mock",
            "--out",
            "output/weather.uri.graph.yaml",
        ),
        "mock",
        category="workflow",
        timeout_s=120,
    ),
    CommandSpec(
        "ex15pw-playwright",
        "15pw",
        "uri3 run-flow current weather health with playwright",
        ("python3", "scripts/examples/effective_weather_playwright.py"),
        "real",
        ("playwright", "weather_agent"),
        "browser",
        180,
    ),
    CommandSpec(
        "ex16-llm",
        "16",
        "llm graph planner with OPENROUTER",
        ("bash", "examples/16_llm_graph_planner/run.sh"),
        "real",
        ("openrouter",),
        "llm",
        180,
    ),
    CommandSpec(
        "ex16www-playwright",
        "16www",
        "landing monitor workflow (playwright)",
        (
            "python3",
            "scripts/examples/run_uri3_workflow.py",
            "examples/16_www_landing_monitor/task_graph.yaml",
            "--approve",
            "--browser",
            "playwright",
        ),
        "real",
        ("www_8788", "playwright"),
        "monitor",
        180,
    ),
    CommandSpec(
        "ex16www-monitor-landing",
        "16www",
        "monitor_landing.py price/uptime check",
        ("python3", "scripts/www/monitor_landing.py", "--url", "http://localhost:8788/www/"),
        "real",
        ("www_8788",),
        "monitor",
        60,
    ),
    CommandSpec(
        "ex16www-monitor-url-down",
        "16www",
        "monitor_url.py PAGE_DOWN notify (local probe)",
        ("python3", "scripts/www/monitor_url.py", "--url", "http://127.0.0.1:1/www/", "--notify"),
        "real",
        (),
        "monitor",
        30,
    ),
    CommandSpec(
        "ex18-llm",
        "18",
        "llm flow planner with OPENROUTER",
        ("bash", "examples/18_llm_flow_planner/run.sh"),
        "real",
        ("openrouter",),
        "llm",
        180,
    ),
    CommandSpec(
        "ex30-www-smoke",
        "30",
        "WWW chat API ask dry-run",
        (
            "curl",
            "-sf",
            "-X",
            "POST",
            "http://localhost:8788/api/ask",
            "-H",
            "Content-Type: application/json",
            "-d",
            '{"prompt":"show weather-map-agent process","dry_run":true}',
        ),
        "real",
        ("www_8788", "curl"),
        "chat",
        30,
    ),
    CommandSpec(
        "ex32-explain-real",
        "32",
        "uri explain ecommerce integration (no mock)",
        ("uri", "explain", "workflow://ecommerce/woocommerce/sync"),
        "dry-run",
        ("cli_uri",),
        "ecommerce",
    ),
    CommandSpec(
        "ex33-ask-supplier",
        "33",
        "uri ask supplier report (office card)",
        (
            "uri",
            "ask",
            "Wejdź na stronę dostawcy, pobierz raport CSV za ten miesiąc i zapisz w rozliczeniach.",
        ),
        "dry-run",
        ("cli_uri",),
        "office",
    ),
)

ALL_COMMANDS = DEFAULT_COMMANDS + REAL_COMMANDS

# Ensure every catalog example has at least one default command
_catalog_ids = {spec.id for spec in ALL_EXAMPLES}
_command_example_ids = {cmd.example_id for cmd in DEFAULT_COMMANDS}
_missing = _catalog_ids - _command_example_ids
assert not _missing, f"missing default commands for example ids: {_missing}"
