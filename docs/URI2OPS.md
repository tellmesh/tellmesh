# uri2ops

`uri2ops` to samodzielny pakiet **URI Operation Registry + Operator Runtime**.
Po splicie monorepo źródło pakietu jest poza tym repozytorium: w tym
workspace lokalny checkout jest pod `/home/tom/github/tellmesh/uri2ops`, a
odpowiadające repo upstream to [`tellmesh/uri2ops`](https://github.com/tellmesh/uri2ops).
Ten repozytorium używa pakietu przez `tool.uv.sources` w
[`pyproject.toml`](../pyproject.toml).

Hypervisor **nie klika, nie pisze i nie steruje OS** — wykonanie operatora należy do `uri2ops`.

## Architektura

```txt
nl2uri     → URI task/workflow graph (single, list, tree, task, graph)
uri3       → parsing, validation, semantic routing, uri3 run-workflow
hypervisor → deployment, lifecycle, policy, audit, operator/environment routing
uri2run    → transport dispatch
uri2ops    → operation registry + adapters + policy + artifacts + serve
```

Pełna dokumentacja pakietu: [`tellmesh/uri2ops`](https://github.com/tellmesh/uri2ops).

## CLI

```bash
uri2ops operations list
uri2ops operations describe browser open
uri2ops validate examples/10_browser_operator/task.health.yaml
uri2ops plan examples/10_browser_operator/task.health.yaml
uri2ops run examples/10_browser_operator/task.health.yaml --adapter mock --approve
uri2ops run examples/10_browser_operator/task.health.yaml --adapter playwright --approve
uri2ops run examples/10_browser_operator/task.health.yaml --adapter auto --approve
uri2ops serve --host 127.0.0.1 --port 8795
uri2ops registry list
uri2ops registry validate
```

### Adaptery (`--adapter`)

| Wartość | Opis |
|---------|------|
| `mock` | Deterministyczne mocki (testy, CI) |
| `playwright` | Prawdziwa przeglądarka (extra `[browser]`) |
| `adb` | Android przez ADB + UI Automator |
| `uia` | Windows UI Automation (extra `[windows]`) |
| `auto` | Wybór real backend gdy dostępny, inaczej mock |

## Schematy URI operatora

```txt
browser://chrome/page/open
browser://chrome/page/active
android://device/{id}/screenshot|dump_ui|tap
pcwin://window/{id}/focus
pcwin://control/{automation_id}/click
assertion://contains
artifact://operator/workflows/{task_id}/{run_id}/{step_id}/...
```

## Konfiguracja

| Plik | Rola |
|------|------|
| [`config/operator_policy.uri.yaml`](../config/operator_policy.uri.yaml) | Polityka approve/risk |
| [`config/operator_registry.uri.yaml`](../config/operator_registry.uri.yaml) | Bazowy rejestr operacji (CLI merge) |
| [`config/extra_operator_registry.yaml`](../config/extra_operator_registry.yaml) | Rozszerzenia (merge) |
| installed `uri2ops/operation_registry/registry.yaml` | Union registry dla CLI/testów |
| [`agents/operators/*/operation_registry.yaml`](../agents/operators/) | Per-agent registry używany przez deployment |

## HTTP daemon (v0.5)

Deployed operator agents start via `agents/operators/<name>/main.py` (uvicorn)
and are selected by `hypervisor.routing` for operator URI schemes:

| Deployment | Schemes | Declared port |
|------------|---------|---------------|
| `browser-operator.local` | `browser://`, `dom://` | 8793 |
| `desktop-operator.local` | `screen://`, `input://`, `pcwin://`, `android://` | 8791 |
| `device-robot-operator.local` | `robot://`, `device://` | 8792 |

The `uri2ops serve` CLI remains for local dev and union-registry workflows. Use
a free port so it does not collide with dedicated operator agents:

```bash
hypervisor run-agent browser-operator.local --detach --wait-healthy
# or direct:
uvicorn agents.operators.browser_operator.main:app --host 127.0.0.1 --port 8793

uri2ops serve --port 8795   # union registry (dev/CLI)
curl http://127.0.0.1:8795/health
curl http://127.0.0.1:8795/registry
curl -X POST http://127.0.0.1:8795/run -H 'Content-Type: application/json' -d @task.json
```

A2A: `/.well-known/agent-card.json`, `POST /a2a/tasks`  
MCP: `GET /mcp/tools`, `POST /mcp/tools/call`

Przykład: [`examples/14_uri2ops_serve/`](../examples/14_uri2ops_serve/README.md).

## Przykłady

| # | Katalog | Temat |
|---|---------|-------|
| 10 | [`examples/10_browser_operator/`](../examples/10_browser_operator/) | Mock browser + assertion |
| 11 | [`examples/11_playwright_browser/`](../examples/11_playwright_browser/) | Playwright |
| 12 | [`examples/12_android_operator/`](../examples/12_android_operator/) | Android ADB |
| 13 | [`examples/13_pcwin_operator/`](../examples/13_pcwin_operator/) | Windows UIA |
| 14 | [`examples/14_uri2ops_serve/`](../examples/14_uri2ops_serve/) | HTTP daemon |

## Powiązane dokumenty

- [`docs/OPERATOR_RUNTIME.md`](./OPERATOR_RUNTIME.md) — przepływ wykonania
- [`docs/URI_OPERATION_REGISTRY.md`](./URI_OPERATION_REGISTRY.md) — format registry
- [`docs/OPERATOR_SECURITY.md`](./OPERATOR_SECURITY.md) — zasady bezpieczeństwa
- [`tellmesh/uri2ops`](https://github.com/tellmesh/uri2ops)
