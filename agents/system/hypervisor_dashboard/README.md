# hypervisor-dashboard (system agent)

TellMesh control plane (:8788) — observer, renderer, and approval-gated URI controller.

| Layer | Location |
|-------|----------|
| Contract | [`hypervisor_dashboard.yaml`](hypervisor_dashboard.yaml) |
| Deployment entry | `agents.system.hypervisor_dashboard.main:app` |
| Implementation | `hypervisor_dashboard_agent/` (this directory) |

## Run

```bash
hypervisor run-agent hypervisor-dashboard.local --detach --wait-healthy
uvicorn agents.system.hypervisor_dashboard.main:app --host 0.0.0.0 --port 8788
```

## Endpoints

| Path | Role |
|------|------|
| `GET /www/` | static chat UI from repo `www/` |
| `GET /ui/agents` | agent list |
| `POST /api/ask` | `urish ask` NL planning |
| `POST /api/uri/call` | policy-gated URI execution |
| `GET /api/events` | observable events stream |
