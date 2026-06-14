# 15 — Playwright browser adapter (optional)

Real browser automation przez Playwright zamiast mock adaptera.

## Instalacja

```bash
pip install -e '.[browser]'
playwright install chromium
```

## Uruchomienie

```bash
# mock (domyślnie gdy brak Playwright)
uri3 run-workflow examples/14_workflow_executor_mock/task_graph.yaml --approve --browser mock

# Playwright (headless Chromium)
uri3 run-workflow examples/14_workflow_executor_mock/task_graph.yaml --approve --browser playwright
```

Zmienna środowiskowa:

```bash
export URI3_BROWSER_ADAPTER=playwright   # auto | mock | playwright
```

## Artefakty

Pliki trafiają do:

```txt
output/artifacts/workflows/{workflow_id}/{run_id}/{step_id}/
  open.json
  dom.json
  screenshot.png
```

URI w wynikach: `artifact://operator/workflows/...`

## Test e2e Playwright

```bash
URI3_PLAYWRIGHT_E2E=1 pytest tests/uri3/test_browser_adapter.py -k playwright -q
```

## Operacje

| URI | Operacja | Efekt |
|-----|----------|-------|
| `browser://chrome/page/open` | `open` | `page.goto`, zapis `open.json` |
| `dom://chrome/active/body` | `read` / `extract_dom` | `inner_text` + `content` → `dom.json` |
| `screen://browser/active/screenshot` | `capture` | PNG → `screenshot.png` |

Sesja przeglądarki jest współdzielona między krokami workflow i zamykana w `finally` po `run-workflow`.
