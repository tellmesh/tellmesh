# Scripts (migrated to TellMesh)

Build, CI, examples and migration scripts live in TellMesh package repos:

| Was | Now |
|-----|-----|
| `scripts/www/` | [`tellmesh/www/scripts/`](../../tellmesh/www/scripts/) |
| `scripts/examples/`, `scripts/ci/`, `scripts/architecture_audit/` | [`tellmesh/resource-agent-hypervisor/scripts/`](../../tellmesh/resource-agent-hypervisor/scripts/) |
| `scripts/tellmesh/` | [`tellmesh/resource-agent-hypervisor/scripts/tellmesh/`](../../tellmesh/resource-agent-hypervisor/scripts/tellmesh/) |
| `scripts/fix-generated-ownership.sh` | [`tellmesh/resource-agent-factory/scripts/`](../../tellmesh/resource-agent-factory/scripts/) |
| `run_uri3_workflow.py` | [`tellmesh/uri3/scripts/`](../../tellmesh/uri3/scripts/) |

The root [`Makefile`](../Makefile) uses `TELLMESH_ROOT` / `WWW_SCRIPTS` / `HV_SCRIPTS` variables.

**Compatibility shims** (forward to tellmesh — used by `examples/*/run.sh`):

| Shim | Forwards to |
|------|-------------|
| `scripts/ci/ensure_editable_install.sh` | `tellmesh/resource-agent-hypervisor/scripts/ci/` |
| `scripts/examples/cli_fallback.sh` | `tellmesh/resource-agent-hypervisor/scripts/examples/` |
| `scripts/www/*` | `tellmesh/www/scripts/` |

```bash
make www-docs          # → tellmesh/www/scripts/*
make architecture-gate # → tellmesh/resource-agent-hypervisor/scripts/ci/*
python3 ../../tellmesh/resource-agent-hypervisor/scripts/tellmesh/sync_www.py
```
