# codex-nl-smoke-agent

Generated from NL prompt: stworz nowego agenta codex-nl-smoke-agent, ktory czyta file:// README, sprawdza device://device/sensor-1/status i ma komende cron monitor

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest codex-nl-smoke-agent.local`

```markpact:agent codex-nl-smoke-agent
version: 1
agent:
  id: agent://codex-nl-smoke-agent
  name: codex-nl-smoke-agent
  implementation: generated
  contract: contracts/agents/codex_nl_smoke_agent.yaml
  package: agents/generated/codex_nl_smoke_agent
  module: agents.generated.codex_nl_smoke_agent.main:app
  version: 0.1.0
  python_package: codex_nl_smoke_agent
  description: 'Generated from NL prompt: stworz nowego agenta codex-nl-smoke-agent,
    ktory czyta file:// README, sprawdza device://device/sensor-1/status i ma komende
    cron monitor'
capabilities:
- name: read_markpact_source
  type: resource_read
  uri: file:///home/tom/github/wronai/hypervisor/agents/generated/codex_nl_smoke_agent/README.md
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
  command: RunCronMonitor
  input_schema: app.codex.v1.RunCronMonitorCommand
  emits:
  - CronMonitorRequested
  description: Dispatch a scheduled monitor command.
```

```markpact:deployment codex-nl-smoke-agent.local
deployment:
  id: codex-nl-smoke-agent.local
  agent_ref: agent://codex-nl-smoke-agent
  target_uri: local://agents/generated/codex_nl_smoke_agent
  status: generated
  health_uri: http://localhost:8130/health
  card_uri: http://localhost:8130/.well-known/agent-card.json
  view_uri: view://process/agent/codex-nl-smoke-agent.local/latest
metadata:
  source: nl_agent_factory
  contract: contracts/agents/codex_nl_smoke_agent.yaml
runtime:
  run: hypervisor run-agent codex-nl-smoke-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent codex-nl-smoke-agent.local
  describe: hypervisor describe-agent codex-nl-smoke-agent.local
supervise:
  once: hypervisor supervise codex-nl-smoke-agent.local --repair auto
  watch: hypervisor supervise codex-nl-smoke-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=codex-nl-smoke-agent.local
  process: log://file/output/logs/agents/codex-nl-smoke-agent.local.process.log
manifest:
  self: markpact://agents/manifests/codex-nl-smoke-agent.markpact.md
```

```markpact:runtime codex-nl-smoke-agent.local
runtime:
  module: agents.generated.codex_nl_smoke_agent.main:app
  path: /home/tom/github/wronai/hypervisor/agents/generated/codex_nl_smoke_agent
  port: 8130
  health_uri: http://localhost:8130/health
  card_uri: http://localhost:8130/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.generated.codex_nl_smoke_agent.main:app
    --host 0.0.0.0 --port 8130
```

```markpact:docker codex-nl-smoke-agent
service:
  name: codex-nl-smoke-agent
  build:
    context: .
    dockerfile: agents/generated/codex_nl_smoke_agent/Dockerfile
  container_name: codex-nl-smoke-agent
  ports:
  - 8130:8130
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8130/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/codex-nl-smoke-agent/docker-compose.yaml
```
