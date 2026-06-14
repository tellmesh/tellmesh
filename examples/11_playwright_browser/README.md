# Example 11 — uri2ops Playwright browser operator (v0.2)

Requires:

```bash
pip install -e '.[browser]'
playwright install chromium
```

Mock run (default):

```bash
python -m uri2ops.cli run examples/10_browser_operator/task.health.yaml --adapter mock --approve
```

Playwright run against a local HTTP server:

```bash
bash examples/11_playwright_browser/run.sh
```

Optional e2e test:

```bash
URI2OPS_PLAYWRIGHT_E2E=1 python -m pytest tests/test_uri2ops_browser.py::test_playwright_task_executes_against_local_server -v
```

Auto adapter picks Playwright when Chromium is installed, otherwise mock:

```bash
python -m uri2ops.cli run examples/10_browser_operator/task.health.yaml --adapter auto --approve
```
