# generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent

generuj mape pogody dwa tygodnie do przodu w html

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local`

```markpact:agent generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
version: 1
agent:
  id: agent://generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
  name: generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
  implementation: generated
  contract: contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
  package: agents/generated/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent
  module: agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.main:app
  version: 0.1.0
  python_package: generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent
  description: generuj mape pogody dwa tygodnie do przodu w html
capabilities:
- name: run
  type: command
  command: RunTask
  input_schema: app.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html.v1.RunTaskCommand
  emits:
  - TaskRequested
  - TaskCompleted
```

```markpact:deployment generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
deployment:
  id: generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
  agent_ref: agent://generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
  target_uri: local://agents/generated/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent
  status: generated
  health_uri: http://localhost:8101/health
  card_uri: http://localhost:8101/.well-known/agent-card.json
  view_uri: view://process/agent/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local/latest
metadata:
  source: uri_tree
  domain_id: generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html
runtime:
  run: hypervisor run-agent generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
    --detach --wait-healthy
  inspect: hypervisor inspect-agent generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
  describe: hypervisor describe-agent generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
supervise:
  once: hypervisor supervise generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
    --repair auto
  watch: hypervisor supervise generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
    --watch --repair auto --interval 15
logs:
  hypervisor: log://hypervisor?grep=generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
  process: log://file/output/logs/agents/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local.process.log
manifest:
  self: markpact://agents/manifests/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.markpact.md
```

```markpact:runtime generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent.local
runtime:
  module: agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.main:app
  path: /home/tom/github/tellmesh/tellmesh/agents/generated/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent
  port: 8101
  health_uri: http://localhost:8101/health
  card_uri: http://localhost:8101/.well-known/agent-card.json
  command: /home/tom/github/tellmesh/tellmesh/.venv/bin/python3 -m uvicorn agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.main:app
    --host 0.0.0.0 --port 8101
```

```markpact:docker generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
service:
  name: generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
  build:
    context: .
    dockerfile: agents/generated/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent/Dockerfile
  container_name: generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent
  ports:
  - 8101:8101
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8101/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent/docker-compose.yaml
```
