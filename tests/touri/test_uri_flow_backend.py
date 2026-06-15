"""Tests for touri uri_flow and uri_graph backends."""

from __future__ import annotations

from pathlib import Path

from touri.executor import call_uri
from uri2run.transports.graph_transport import run_uri_graph


def test_uri_flow_backend_dry_run(repo_root: Path):
    registry = repo_root / "examples" / "20_touri_capabilities"
    result = call_uri("workflow://flow/weather/dry-run", registry, context={"root": repo_root})
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["capability"] == "workflow.weather.flow"
    assert payload["backend"] == "uri_flow"
    assert payload["result_type"] == "plan"
    assert payload["data"]["plan"]["graph_id"] == "weather-agent-local-health"


def test_uri_graph_backend_dry_run(repo_root: Path):
    registry = repo_root / "examples" / "20_touri_capabilities"
    result = call_uri(
        "workflow://graph/check-agent-health/dry-run",
        registry,
        context={"root": repo_root},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["capability"] == "workflow.check_health.graph"
    assert payload["backend"] == "uri_graph"
    assert payload["result_type"] == "plan"
    assert payload["data"]["plan"]["graph_id"] == "check-agent-health"


def test_uri_graph_backend_website_screenshot_schedule(repo_root: Path):
    registry = repo_root / "examples" / "20_touri_capabilities"
    result = call_uri(
        "workflow://graph/website-screenshot-schedule/dry-run",
        registry,
        context={"root": repo_root},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["capability"] == "workflow.website_screenshot_schedule.dry_run"
    assert payload["backend"] == "uri_graph"
    assert payload["result_type"] == "plan"
    assert payload["data"]["plan"]["graph_id"] == "website-screenshot-schedule"


def test_uri_graph_execution_writes_artifacts_to_context_root(tmp_path: Path):
    graph_dir = tmp_path / "readonly_graphs"
    graph_dir.mkdir()
    graph_path = graph_dir / "task.yaml"
    graph_path.write_text(
        """
task:
  id: readonly-root-graph
  description: Browser graph loaded from a read-only source directory.
steps:
  - id: open_page
    uri: browser://chrome/page/open
    operation: open
    kind: command
    payload:
      url: https://example.com/reports
  - id: read_page
    uri: dom://chrome/active/body
    operation: read
    kind: query
    depends_on:
      - open_page
""",
        encoding="utf-8",
    )
    runtime_root = tmp_path / "runtime"
    runtime_root.mkdir()

    graph_dir.chmod(0o555)
    try:
        result = run_uri_graph(
            str(graph_path),
            {"approve": True, "dry_run": False, "browser": "mock"},
            {"root": str(runtime_root)},
        )
    finally:
        graph_dir.chmod(0o755)

    payload = result.to_dict()
    assert payload["ok"] is True
    assert not (graph_dir / "output").exists()
    assert (runtime_root / "output" / "artifacts" / "workflows" / "readonly-root-graph").exists()


def test_uri_graph_office_supplier_readonly_examples_dir(tmp_path: Path):
    """Mirror www Docker: examples/ is read-only; writes must go to repo output/."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "contracts").mkdir()
    (repo / "schemas").mkdir()
    graph_dir = repo / "examples" / "33_office_workflows"
    graph_dir.mkdir(parents=True)
    graph_path = graph_dir / "supplier_report_monthly.yaml"
    graph_path.write_text(
        """
task:
  id: office-supplier-report-monthly
  description: Supplier portal monthly CSV (readonly examples dir).
steps:
  - id: open_portal
    uri: browser://chrome/page/open
    operation: open
    kind: command
    payload:
      url: https://supplier-portal.example.local/reports/monthly
""",
        encoding="utf-8",
    )

    graph_dir.chmod(0o555)
    try:
        result = run_uri_graph(
            "examples/33_office_workflows/supplier_report_monthly.yaml",
            {"approve": True, "dry_run": False, "browser": "mock"},
            {"root": str(repo), "artifact_root": str(repo)},
        )
    finally:
        graph_dir.chmod(0o755)

    payload = result.to_dict()
    assert payload["ok"] is True
    assert not (graph_dir / "output").exists()
    assert (
        repo
        / "output"
        / "artifacts"
        / "workflows"
        / "office-supplier-report-monthly"
    ).exists()
