# codex-nl-plan-agent

Generated from NL prompt: stworz nowego agenta codex-nl-plan-agent, ktory czyta file:// README, sprawdza device://device/sensor-1/status i ma komende cron monitor

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest codex-nl-plan-agent.local`

```markpact:agent codex-nl-plan-agent
version: 1
agent:
  id: agent://codex-nl-plan-agent
  name: codex-nl-plan-agent
  implementation: generated
  contract: contracts/agents/codex_nl_plan_agent.yaml
  package: agents/generated/codex_nl_plan_agent
  module: agents.generated.codex_nl_plan_agent.main:app
  version: 0.1.0
  python_package: codex_nl_plan_agent
  description: 'Generated from NL prompt: stworz nowego agenta codex-nl-plan-agent,
    ktory czyta file:// README, sprawdza device://device/sensor-1/status i ma komende
    cron monitor'
capabilities:
- name: read_markpact_source
  type: resource_read
  uri: file:///app/agents/generated/codex_nl_plan_agent/README.md
  output_schema: app.codex.v1.MarkpactSourceView
  renderer: text
  description: Read generated agent README/provenance through file://.
- name: read_device_status
  type: resource_read
  uri: device://device/sensor-1/status
  output_schema: operator.device.v1.DeviceStatus
  renderer: detail
  description: Read device status through uri2ops.
- name: run_cron_monitor
  type: command
  uri: cron://www/monitor/landing
  command: RunCronMonitor
  input_schema: app.codex.v1.RunCronMonitorCommand
  emits:
  - CronMonitorRequested
  description: Dispatch a scheduled monitor through cron:// URI.
```

```markpact:deployment codex-nl-plan-agent.local
deployment:
  id: codex-nl-plan-agent.local
  agent_ref: agent://codex-nl-plan-agent
  target_uri: local://agents/generated/codex_nl_plan_agent
  status: generated
  health_uri: http://localhost:8132/health
  card_uri: http://localhost:8132/.well-known/agent-card.json
  view_uri: view://process/agent/codex-nl-plan-agent.local/latest
metadata:
  source: nl_agent_factory
  contract: contracts/agents/codex_nl_plan_agent.yaml
runtime:
  run: hypervisor run-agent codex-nl-plan-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent codex-nl-plan-agent.local
  describe: hypervisor describe-agent codex-nl-plan-agent.local
supervise:
  once: hypervisor supervise codex-nl-plan-agent.local --repair auto
  watch: hypervisor supervise codex-nl-plan-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=codex-nl-plan-agent.local
  process: log://file/output/logs/agents/codex-nl-plan-agent.local.process.log
manifest:
  self: markpact://agents/manifests/codex-nl-plan-agent.markpact.md
```

```markpact:runtime codex-nl-plan-agent.local
runtime:
  module: agents.generated.codex_nl_plan_agent.main:app
  path: /home/tom/github/tellmesh/tellmesh/agents/generated/codex_nl_plan_agent
  port: 8132
  health_uri: http://localhost:8132/health
  card_uri: http://localhost:8132/.well-known/agent-card.json
  command: /home/tom/github/tellmesh/tellmesh/.venv/bin/python3 -m uvicorn agents.generated.codex_nl_plan_agent.main:app
    --host 0.0.0.0 --port 8132
```

```markpact:docker codex-nl-plan-agent
service:
  name: codex-nl-plan-agent
  build:
    context: .
    dockerfile: agents/generated/codex_nl_plan_agent/Dockerfile
  container_name: codex-nl-plan-agent
  ports:
  - 8132:8132
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8132/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/codex-nl-plan-agent/docker-compose.yaml
```
