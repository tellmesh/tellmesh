# URI Operation Registry

Rejestr operacji mapuje schematy URI i nazwy operacji na handlery, semantykę CQRS i schematy wejścia/wyjścia.

- **Scheme registry** (uri3): „Czy `browser://…` jest poprawnym URI?”
- **Operation registry** (uri2ops): „Co mogę zrobić z `browser://…`, jaki schema waliduje payload i jaki handler to wykonuje?”

## Lokalizacja plików

```txt
installed uri2ops/operation_registry/registry.yaml          # kanoniczny union registry
agents/operators/*/operation_registry.yaml                 # registry per operator-agent
config/operator_registry.uri.yaml                          # źródła merge dla serve / remote
config/extra_operator_registry.yaml                        # rozszerzenia projektu
schemas/operator_registry.schema.json                      # JSON Schema walidacji
```

## Przykład wpisu

```yaml
version: 1
schemes:
  browser:
    operations:
      open:
        kind: command
        handler: python://agents.operators.browser_operator.adapters.browser_router:open_page
        input_schema: operator.browser.v1.BrowserPageOpenCommand
        output_schema: operator.common.v1.OperationResult
        side_effects: true
        requires_policy: true
        adapters: [mock, playwright]
      extract_dom:
        kind: query
        handler: python://agents.operators.browser_operator.adapters.browser_router:extract_dom
        output_schema: operator.browser.v1.DomSnapshot
        side_effects: false
        produces_artifact: true
        adapters: [mock, playwright]
```

Handlery real backendów są w routerach (`browser_router`, `android_router`, `pcwin_router`) — wybór mock vs real przez `--adapter auto`.

## Semantyka CQRS

| `kind` | Mutacja | Policy |
|--------|---------|--------|
| `query` | tylko odczyt | domyślnie bez approve |
| `command` | może mutować stan zewnętrzny | `requires_policy: true` → `--approve` |

## Remote registry (v0.5)

`uri2ops serve`, `resolve_operation_registry()` and semantic URI explain read
`config/operator_registry.uri.yaml` as source configuration. In the current
repo the local source is the default registry shipped with the installed
`uri2ops` package, plus this project extension:

1. installed `uri2ops/operation_registry/registry.yaml`
2. `config/extra_operator_registry.yaml`

```bash
uri2ops registry list
uri2ops registry validate
curl http://127.0.0.1:8795/registry
```

## Protobuf / JSON Schema

Kontrakty operatora: [`contracts/proto/operator/`](../contracts/proto/operator/)

- `browser.proto`, `android.proto`, `common.proto`, `events.proto`, …

## Zasady

- `query` nie mutuje stanu zewnętrznego.
- `command` wymaga polityki approve (chyba że jawnie wyłączone w policy).
- Duże wyniki → `artifact://`, nie payload eventu.
- Sekrety nigdy w event log (redaction w `uri2ops/operator/redaction.py`).

## Powiązane

- [`docs/URI2OPS.md`](./URI2OPS.md)
- [`docs/OPERATOR_RUNTIME.md`](./OPERATOR_RUNTIME.md)
- [`docs/OPERATOR_SECURITY.md`](./OPERATOR_SECURITY.md)
- [`config/operator_policy.uri.yaml`](../config/operator_policy.uri.yaml)
