# Agent Markpact manifests

One portable file per agent under `agents/manifests/<agent-name>.markpact.md`.

Each manifest consolidates data that was previously spread across:

| Block | Source (compiled from) |
|-------|------------------------|
| `markpact:agent` | `contracts/agents/*.yaml` or operator YAML + capabilities |
| `markpact:deployment` | `deployments/agent_deployments.yaml` |
| `markpact:runtime` | `local_targets.build_local_run_plan` |
| `markpact:docker` | `agents/*/Dockerfile` + `config/docker.uri.yaml` |

Manifests are **sync outputs** today — canonical runtime paths remain
`contracts/`, `deployments/`, and `agents/{generated,custom,system,operators}/`.

Materialize Docker Compose from a manifest:

```bash
hypervisor materialize-agent-compose agents/manifests/weather-map-agent.markpact.md
docker compose -f output/deployments/weather-map-agent/docker-compose.yaml up -d --build
```

## Sync

```bash
hypervisor sync-agent-manifest weather-map-agent.local
hypervisor sync-agent-manifests
```

## Materialize / validate

```bash
hypervisor materialize-agent agents/manifests/weather-map-agent.markpact.md
hypervisor materialize-agent agents/manifests/new-agent.markpact.md --write-contract
```

## Load in Python

```python
from pathlib import Path
from uri2pact import extract_markpact_blocks

text = Path("agents/manifests/weather-map-agent.markpact.md").read_text()
for block in extract_markpact_blocks(text, "deployment"):
    print(block["body"])
```

See [`docs/MARKPACT_WITH_TOURI.md`](../docs/MARKPACT_WITH_TOURI.md) for the broader Markpact model.
