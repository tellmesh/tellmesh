# Hypervisor monorepo — Python packages

All Python packages live in the **TellMesh product org** under `~/github/tellmesh/`:

| TellMesh repo | Distribution | Modules |
|---|---|---|
| [`tellmesh/uri3`](../../tellmesh/uri3) | `uri3` | `uri3` |
| [`tellmesh/nl2uri`](../../tellmesh/nl2uri) | `nl2uri` | `nl2uri`, `nl2a` |
| [`tellmesh/uri2flow`](../../tellmesh/uri2flow) | `uri2flow` | `uri2flow` |
| [`tellmesh/uri2ops`](../../tellmesh/uri2ops) | `uri2ops` | `uri2ops` |
| [`tellmesh/uri2voice`](../../tellmesh/uri2voice) | `uri2voice` | `uri2voice` |
| [`tellmesh/uri2pact`](../../tellmesh/uri2pact) | `uri2pact` | `uri2pact` |
| [`tellmesh/uri2run`](../../tellmesh/uri2run) | `uri2run` | `uri2run` |
| [`tellmesh/uri2verify`](../../tellmesh/uri2verify) | `uri2verify` | `uri2verify` |
| [`tellmesh/urigen`](../../tellmesh/urigen) | `urigen` | `urigen` |
| [`tellmesh/touri`](../../tellmesh/touri) | `touri` | `touri`, `touri_examples` |
| [`tellmesh/urish`](../../tellmesh/urish) | `urish` | `urish` |
| [`tellmesh/resource-agent-hypervisor`](../../tellmesh/resource-agent-hypervisor) | `resource-agent-hypervisor` | `hypervisor`, `meta_agent`, `runtime_client` |
| [`tellmesh/resource-agent-factory`](../../tellmesh/resource-agent-factory) | `resource-agent-factory` | `generator` |
| [`tellmesh/hypervisor-dashboard`](../../tellmesh/hypervisor-dashboard) | `hypervisor-dashboard-agent` | `hypervisor_dashboard_agent` |

This directory keeps only analysis cache (`project/`) and migration scripts reference paths.

Shared repo assets remain at the hypervisor root:

```txt
contracts/ schemas/ domains/ agents/ deployments/ config/ examples/ output/ tests/
```

## Install

From hypervisor repo root (requires `~/github/tellmesh/*` sibling checkout):

```bash
pip install -e '.[dev]'
# or
uv sync
```

Path sources: root [`pyproject.toml`](../pyproject.toml) → `[tool.uv.sources]`.

## Split / sync scripts

```bash
python ../../tellmesh/resource-agent-hypervisor/scripts/tellmesh/split_core_packages.py
python ../../tellmesh/resource-agent-hypervisor/scripts/tellmesh/sync_www.py
python ../../tellmesh/resource-agent-hypervisor/scripts/tellmesh/move_tests.py
```

Deploy glue for WWW chat: [`www/README.md`](../www/README.md).
