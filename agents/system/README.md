# System agents

Control-plane agents with thin deployment entry under `agents/system/`.

| Agent | Entry | Implementation |
|-------|-------|----------------|
| hypervisor-dashboard | `agents.system.hypervisor_dashboard.main:app` | `agents/system/hypervisor_dashboard/hypervisor_dashboard_agent/` |

Hypervisor resolves `local://agents/system/<package>` via `local_target_to_module()`.
