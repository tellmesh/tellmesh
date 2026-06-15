# Browser Ops domain

Canonical YAML registry: [`scenario_registry.yaml`](./scenario_registry.yaml)

This domain pack describes generic browser-operation routing. It does not
execute browser actions directly. Execution stays in `uri2ops`, lifecycle stays
in `hypervisor`, and the generic operator contract stays in
[`agents/operators/browser_operator.yaml`](../../agents/operators/browser_operator.yaml).

## Files

| File | Purpose |
|------|---------|
| [`domain.yaml`](./domain.yaml) | Boundary and ownership contract |
| [`operator_registry.yaml`](./operator_registry.yaml) | Browser capability cards |
| [`scenario_registry.yaml`](./scenario_registry.yaml) | NL routing to browser operator URIs |

## Approval boundary

`browser_ops` is an orchestration domain, not the executor. Mutating browser
URIs are policy-gated in `urish.policy` and require either dry-run planning or
explicit approval:

| Read URI examples | Mutation URI examples |
|-------------------|-----------------------|
| `browser://chrome/page/active/dom` | `browser://chrome/page/open` |
| `browser://chrome/page/active/screenshot` | `browser://chrome/page/active/click` |

Execution environments (`local`, `python`, `docker`, `remote`) are selected at
call time via MCP/A2A arguments or payload. Machine-readable profiles live in
[`config/runtime_environments.yaml`](../../config/runtime_environments.yaml).

## Load from markpact

```markpact:scenario_registry browser-ops
include: domains/browser_ops/scenario_registry.yaml
kind: urish.scenario_registry
metadata:
  id: browser-ops
  markpact_readme: domains/browser_ops/README.md
```

See [`docs/DESKTOP_AUTONOMY.md`](../../docs/DESKTOP_AUTONOMY.md) and
[`docs/DOMAIN_SEPARATION.md`](../../docs/DOMAIN_SEPARATION.md).
