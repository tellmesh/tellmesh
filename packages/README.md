# Monorepo packages (v0.5.7)

Physical Python packages live under `packages/`:

| Directory | Distribution | Modules |
|---|---|---|
| `packages/uri3/` | `uri3` | `uri3` |
| `packages/nl2uri/` | `nl2uri` | `nl2uri`, `nl2a` |
| `packages/resource-agent-hypervisor/` | `resource-agent-hypervisor` | `hypervisor`, `meta_agent`, `runtime_client` |
| `packages/resource-agent-factory/` | `resource-agent-factory` | `generator` |

Shared repo assets remain at the repository root:

```txt
contracts/ schemas/ domains/ agents/ deployments/ examples/ output/ tests/
```

## Install

From repo root:

```bash
pip install -e '.[dev]'
```

Or with uv workspace:

```bash
uv sync
```

## CLI entry points

```bash
uri3 --help
nl2uri --help
nl2a --help
hypervisor --help
```

See [`README.md`](../README.md) and [`examples/README.md`](../examples/README.md).
