# Scripts (migrated to TellMesh)

Build, CI, examples and migration scripts live in TellMesh package repos:

| Was | Now |
|-----|-----|
| `scripts/www/` | [`tellmesh/www/scripts/`](../www/scripts/) |
| `scripts/examples/`, `scripts/ci/`, `scripts/architecture_audit/` | [`tellmesh/resource-agent-hypervisor/scripts/`](../resource-agent-hypervisor/scripts/) |
| `scripts/tellmesh/` | [`tellmesh/resource-agent-hypervisor/scripts/tellmesh/`](../resource-agent-hypervisor/scripts/tellmesh/) |
| `scripts/fix-generated-ownership.sh` | [`tellmesh/resource-agent-factory/scripts/`](../resource-agent-factory/scripts/) |
| `run_uri3_workflow.py` | [`tellmesh/uri3/scripts/`](../uri3/scripts/) |

The root [`Makefile`](../Makefile) uses `TELLMESH_ROOT` / `WWW_SCRIPTS` / `HV_SCRIPTS` variables.

Examples use direct paths via [`paths.sh`](paths.sh):

```bash
source "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh"
bash "$ROOT/../resource-agent-hypervisor/scripts/ci/ensure_editable_install.sh"
```

```bash
make www-docs          # → tellmesh/www/scripts/*
make architecture-gate # → tellmesh/resource-agent-hypervisor/scripts/ci/*
python3 ../resource-agent-hypervisor/scripts/tellmesh/sync_www.py
```
