# Operator capability agents — isolated uri2ops runtimes

Each operator is a deployable agent package under `agents/operators/<name>/`:

| Package | Deployment | Port | Schemes |
|---------|------------|------|---------|
| `browser_operator/` | `browser-operator.local` | 8793 | `browser://` |
| `desktop_operator/` | `desktop-operator.local` | 8791 | `screen://`, `input://`, `pcwin://`, `android://` |
| `device_robot_operator/` | `device-robot-operator.local` | 8792 | `robot://`, `device://` |

## Layout (per operator)

```
agents/operators/<operator>/
  <operator>.yaml           # contract (capability agent)
  main.py                   # uvicorn entry: agents.operators.<operator>.main:app
  operation_registry.yaml   # scheme-filtered registry for this agent only
  adapters/                 # operator-specific adapter code
  ../common/                # shared utilities (assertion)
  pyproject.toml            # documents dependency on uri2ops framework
```

Symlinks at `agents/operators/<operator>.yaml` point to the in-package contract for backward compatibility.

## Framework vs agent

| Layer | Location |
|-------|----------|
| NL routing / domain packs | `domains/*/` |
| Operator contracts + adapters + registry | `agents/operators/*/` |
| Shared runtime (A2A, MCP, dispatcher, policy) | `packages/uri2ops/` |

`packages/uri2ops/uri2ops/operation_registry/registry.yaml` remains the **union registry** for CLI and tests; deployed agents load their own `operation_registry.yaml`.

## Start

```bash
hypervisor run-agent browser-operator.local --detach --wait-healthy
hypervisor run-agent desktop-operator.local --detach --wait-healthy
hypervisor run-agent device-robot-operator.local --detach --wait-healthy
```

Or directly:

```bash
uvicorn agents.operators.browser_operator.main:app --host 127.0.0.1 --port 8793
```
