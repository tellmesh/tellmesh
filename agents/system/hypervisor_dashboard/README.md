# Hypervisor dashboard — deploy entry

Python package: [`tellmesh/hypervisor-dashboard`](../../../hypervisor-dashboard) (`hypervisor-dashboard-agent`).

This folder keeps only the deployment entry used by Docker and `hypervisor run-agent`:

```bash
uvicorn agents.system.hypervisor_dashboard.main:app --host 0.0.0.0 --port 8788
```

Implementation lives in `hypervisor_dashboard_agent/` inside the tellmesh package.
