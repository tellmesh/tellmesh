# Desktop Ops domain

Canonical YAML registry: [`scenario_registry.yaml`](./scenario_registry.yaml)

This domain pack describes generic desktop-operation routing for screen,
input, pcwin and Android operations. Browser operations live in
[`domains/browser_ops/`](../browser_ops/).

Execution stays in `uri2ops`, lifecycle stays in `hypervisor`, and the generic
operator contract stays in
[`agents/operators/desktop_operator.yaml`](../../agents/operators/desktop_operator.yaml).

## Files

| File | Purpose |
|------|---------|
| [`domain.yaml`](./domain.yaml) | Boundary and ownership contract |
| [`operator_registry.yaml`](./operator_registry.yaml) | Screen, input, pcwin and Android cards |
| [`scenario_registry.yaml`](./scenario_registry.yaml) | NL routing to desktop operator URIs |

## Approval boundary

| Read URI examples | Mutation URI examples |
|-------------------|-----------------------|
| `screen://desktop/observe` | `input://keyboard/type` |
| `android://device/{id}/screenshot` | `pcwin://window/{id}/focus` |
| `android://device/{id}/dump_ui` | `pcwin://control/{id}/click` |
| | `android://device/{id}/tap` |

Browser URIs (`browser://...`) are owned by [`domains/browser_ops/`](../browser_ops/)
and executed by `agent://browser-operator` on port 8793.

See [`docs/DESKTOP_AUTONOMY.md`](../../docs/DESKTOP_AUTONOMY.md) and
[`docs/DOMAIN_SEPARATION.md`](../../docs/DOMAIN_SEPARATION.md).
