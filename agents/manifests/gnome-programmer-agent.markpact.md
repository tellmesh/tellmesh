# gnome-programmer-agent

Observe and interact with Ubuntu GNOME desktop through desktop-operator.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest gnome-programmer-agent.local`

```markpact:agent gnome-programmer-agent
version: 1
agent:
  id: agent://gnome-programmer-agent
  name: gnome-programmer-agent
  implementation: custom
  contract: contracts/agents/gnome_programmer_agent.yaml
  package: agents/custom/gnome_programmer_agent
  module: agents.custom.gnome_programmer_agent.main:app
  version: 0.1.0
  python_package: gnome_programmer_agent
  description: Observe and interact with Ubuntu GNOME desktop through desktop-operator.
capabilities:
- name: observe_desktop
  type: command
  uri: screen://desktop/observe
  command: ObserveDesktop
  input_schema: app.desktop.v1.ObserveDesktopCommand
  output_schema: app.desktop.v1.DesktopObservation
  renderer: detail
  description: Capture GNOME desktop screenshot and window list via desktop-operator.
- name: type_on_desktop
  type: command
  uri: input://desktop/type
  command: TypeOnDesktop
  input_schema: app.desktop.v1.TypeOnDesktopCommand
  output_schema: app.desktop.v1.DesktopInputResult
  renderer: detail
  description: Type text into focused GNOME window via ydotool/xdotool through desktop-operator.
- name: programmer_session
  type: command
  uri: workflow://desktop/programmer-session
  command: RunProgrammerSession
  input_schema: app.desktop.v1.ProgrammerSessionCommand
  output_schema: app.desktop.v1.ProgrammerSessionResult
  renderer: detail
  description: Observe desktop, optionally type a command snippet, and persist session
    notes.
```

```markpact:deployment gnome-programmer-agent.local
deployment:
  id: gnome-programmer-agent.local
  agent_ref: agent://gnome-programmer-agent
  target_uri: local://agents/custom/gnome_programmer_agent
  status: generated
  health_uri: http://localhost:8136/health
  card_uri: http://localhost:8136/.well-known/agent-card.json
  view_uri: view://process/agent/gnome-programmer-agent.local/latest
metadata:
  source: custom_agent
  role: gnome_programmer
  contract: contracts/agents/gnome_programmer_agent.yaml
runtime:
  run: hypervisor run-agent gnome-programmer-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent gnome-programmer-agent.local
  describe: hypervisor describe-agent gnome-programmer-agent.local
supervise:
  once: hypervisor supervise gnome-programmer-agent.local --repair auto
  watch: hypervisor supervise gnome-programmer-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=gnome-programmer-agent.local
  process: log://file/output/logs/agents/gnome-programmer-agent.local.process.log
manifest:
  self: markpact://agents/manifests/gnome-programmer-agent.markpact.md
```

```markpact:runtime gnome-programmer-agent.local
runtime:
  module: agents.custom.gnome_programmer_agent.main:app
  path: /home/tom/github/tellmesh/tellmesh/agents/custom/gnome_programmer_agent
  port: 8136
  health_uri: http://localhost:8136/health
  card_uri: http://localhost:8136/.well-known/agent-card.json
  command: /home/tom/github/tellmesh/tellmesh/.venv/bin/python3 -m uvicorn agents.custom.gnome_programmer_agent.main:app
    --host 0.0.0.0 --port 8136
```
