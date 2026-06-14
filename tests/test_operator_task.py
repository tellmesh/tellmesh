from pathlib import Path

from uri2ops.operator.runner import plan_task, run_task
from uri2ops.operator.task import load_task
from uri2ops.operator.validator import validate_task_file


def test_task_validates():
    assert validate_task_file("examples/10_browser_operator/task.health.yaml") == []


def test_task_plan():
    task = load_task("examples/10_browser_operator/task.health.yaml")
    plan = plan_task(task)
    assert [p["id"] for p in plan] == ["open_health", "read_dom", "verify_ok"]


def test_task_runs_mock():
    task = load_task("examples/10_browser_operator/task.health.yaml")
    result = run_task(task, adapter="mock", approve=True)
    assert result.ok is True
    assert result.steps[-1].result["ok"] is True
