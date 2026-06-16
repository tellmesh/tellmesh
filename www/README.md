# Hypervisor WWW deploy glue

Static UI lives in the **TellMesh product repo**: [`tellmesh/www`](https://github.com/tellmesh/www) (`~/github/tellmesh/www`).

This folder keeps only Docker/Compose wiring for the chat dashboard container.

## Run locally

```bash
# Requires ~/github/tellmesh/www (or HYPERVISOR_WWW_DIR)
make start
# → http://localhost:8788/www/
```

`HYPERVISOR_WWW_DIR` defaults to `../www` (see root `Makefile`). The compose file mounts that checkout read-only into `/app/www`.

## Files here

| File | Role |
|------|------|
| `Dockerfile` | Build hypervisor-dashboard + runtime deps |
| `docker-compose.yml` | `www-chat` service, volume mounts |

## Generators & docs

Build scripts under `scripts/www/` write to tellmesh via `resolve_www_dir()`:

```bash
make www-docs      # updates tellmesh/www when checkout exists
make www-docs-check
```

Full product site docs: [`tellmesh/www/README.md`](../www/README.md).
