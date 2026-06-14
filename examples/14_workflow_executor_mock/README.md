# 14 — Workflow Executor MVP (mock adapters)

Demonstracja pełnego pipeline'u wykonawczego:

```txt
prompt/graph YAML -> validate -> plan -> run-workflow -> events JSONL
```

## Policy gate

| `kind` | Bez `--approve` | Z `--approve` |
|--------|-----------------|---------------|
| `query` | wykonuje mock | wykonuje mock |
| `assertion` | wykonuje mock | wykonuje mock |
| `command` | **blocked** | wykonuje mock / plan hypervisor |

## Szybki start

```bash
pip install -e '.[dev]'

uri3 validate-workflow examples/14_workflow_executor_mock/task_graph.yaml
uri3 plan-workflow examples/14_workflow_executor_mock/task_graph.yaml
uri3 run-workflow examples/14_workflow_executor_mock/task_graph.yaml --dry-run
uri3 run-workflow examples/14_workflow_executor_mock/task_graph.yaml --approve
```

Pełne demo:

```bash
bash examples/14_workflow_executor_mock/run.sh
```

## Event log

Po wykonaniu:

```txt
output/events/workflows/check-agent-health.jsonl
```

Wpisy: `WorkflowStarted`, `StepStarted`, `StepCompleted`, `StepBlocked`, `WorkflowCompleted`.

## Adaptery (v0.6.1 mock, v0.6.2 + Playwright)

- `browser://`, `dom://`, `screen://` — mock lub Playwright (`--browser auto|mock|playwright`)
- `assertion://contains|equals|...` — logika w `AssertionAdapter`
- `hypervisor://deployment/.../run` — plan/dry-run; z `--approve` deleguje do `build_run_plan`

Playwright: `pip install -e '.[browser]' && playwright install chromium` — patrz [`examples/15_playwright_browser`](../15_playwright_browser/).

## Powiązanie z nl2uri

```bash
nl2uri task -p "otwórz Chrome i sprawdź localhost:8101/health" --validate > /tmp/task.yaml
uri3 run-workflow /tmp/task.yaml --dry-run
uri3 run-workflow /tmp/task.yaml --approve
```

`nl2uri` tylko planuje; `uri3` wykonuje.
