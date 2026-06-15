# Agents

This directory is the project boundary for agent-specific artifacts.

Generic packages such as `urish`, `uri3`, `uri2flow`, `touri` and `hypervisor`
must not embed business-domain facts like invoices, WooCommerce, ZUS, Subiekt or
bank approvals. Those facts live here as contracts, generated agents, scenario
registries and markpact-readable README blocks.

## Layout

| Path | Role |
|------|------|
| `agents/manifests/` | Unified Markpact manifest per agent (sync from contract + deployment) |
| `agents/generated/` | Generated Python agents from `contracts/agents/*.yaml` |
| `agents/generated/runtime_routes.py` | Shared HTTP/runtime helpers for thin generated agents |
| `agents/custom/` | Hand-written extensions outside generated output |
| `agents/operators/` | Capability agents (browser, desktop, device-robot) — contract, registry, adapters |
| `agents/system/` | Control-plane agents (hypervisor-dashboard) — thin deployment entry |
| `agents/scenarios/` | NL scenario registries loaded by `urish` |

## Generate Agents

The source of truth is the contract:

```txt
contracts/agents/<name>.yaml
```

Regenerate all agents:

```bash
PYTHONPATH=packages/resource-agent-factory python -m generator.agent_generator contracts/agents/*.yaml
```

Regenerate one agent:

```bash
PYTHONPATH=packages/resource-agent-factory python -m generator.agent_generator contracts/agents/weather_map_agent.yaml
```

The explicit `PYTHONPATH` avoids accidentally importing an unrelated `generator`
package from another local repository.

## Markpact Provenance

Each generated agent README contains:

- `markpact:agent_generation` with contract, hash, package and generation command,
- `markpact:run_log` with inspection command and `log://` URIs,
- runtime commands for local reproduction.

Example:

```bash
python - <<'PY'
from pathlib import Path
from uri2pact import extract_markpact_blocks

readme = Path("agents/generated/weather_map_agent/README.md").read_text(encoding="utf-8")
for block_type in ("agent_generation", "run_log"):
    print(block_type, extract_markpact_blocks(readme, block_type))
PY
```

`touri` currently consumes `markpact:capability`; these provenance and run-log
blocks are parsed through `uri2pact.extract_markpact_blocks` and keep the README
as the human-visible audit trail.

## Operator Agents

Operator agents are capability contracts. They are allowed to expose browser,
screen, input and device operations, but they must not contain domain scenario
data.

Default desktop capability contract:

```txt
agents/operators/desktop_operator/desktop_operator.yaml
```

It is backed by `agents.operators.desktop_operator.main:app` (uri2ops framework) and documented in
[`docs/DESKTOP_AUTONOMY.md`](../docs/DESKTOP_AUTONOMY.md).

## Scenario Registries

Domain NL routing is declarative:

```bash
urish ask "połącz WooCommerce, BaseLinker i ERP; pokaż błędy w chacie"
```

Default source:

```txt
agents/scenarios/office_automation.yaml
```

Override source for another project:

```bash
URISH_SCENARIO_REGISTRY=/path/to/agents/scenarios urish ask "..."
```
