<!-- AUTO-GENERATED FILE. DO NOT EDIT. -->
<!-- Source: contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml -->
<!-- Contract hash: sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda -->
# generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent

Generated thin resource agent.

- Version: `0.1.0`
- Source: `contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml`
- Contract hash: `sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda`
- Generator: `resource-agent-factory`

## Run

```bash
uvicorn agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.main:app --reload --port 8101
```

## Reproduce

```bash
PYTHONPATH=packages/resource-agent-factory python -m generator.agent_generator contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
```

## Markpact provenance

```markpact:agent_generation generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
agent:
  id: agent://generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
  package: agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent
source:
  contract: contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
  contract_hash: sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda
generator:
  id: resource-agent-factory
  command: PYTHONPATH=packages/resource-agent-factory python -m generator.agent_generator contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
runtime:
  default_run: uvicorn agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.main:app --reload --port 8101
logs:
  hypervisor: log://hypervisor?grep=generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
  process: log://file/output/logs/agents/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local.process.log
```

```markpact:run_log generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local.latest
inspect:
  command: hypervisor inspect-agent generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
  uri: view://process/agent/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local/latest
logs:
  hypervisor: log://hypervisor?grep=generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
  process: log://file/output/logs/agents/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local.process.log
```

## Endpoints

```txt
GET /health
GET /capabilities
GET /.well-known/agent.json
GET /.well-known/agent-card.json
GET /resources/read?uri=...
POST /commands
```

## Capabilities

- `run` — `command`, command: `RunTask`

