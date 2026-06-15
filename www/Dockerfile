# www chat — hypervisor-dashboard-agent + static UI
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY wronai/hypervisor/pyproject.toml wronai/hypervisor/uv.lock wronai/hypervisor/README.md ./
COPY wronai/hypervisor/contracts ./contracts
COPY wronai/hypervisor/schemas ./schemas
COPY wronai/hypervisor/deployments ./deployments
COPY wronai/hypervisor/config ./config
COPY wronai/hypervisor/domains ./domains
COPY wronai/hypervisor/knowledge ./knowledge
COPY wronai/hypervisor/examples ./examples
COPY wronai/hypervisor/agents ./agents

# TellMesh editable path deps (patched to tellmesh/* before uv sync)
COPY tellmesh/resource-agent-hypervisor ./tellmesh/resource-agent-hypervisor
COPY tellmesh/resource-agent-factory ./tellmesh/resource-agent-factory
COPY tellmesh/hypervisor-dashboard ./tellmesh/hypervisor-dashboard
COPY tellmesh/uri3 ./tellmesh/uri3
COPY tellmesh/nl2uri ./tellmesh/nl2uri
COPY tellmesh/uri2flow ./tellmesh/uri2flow
COPY tellmesh/uri2ops ./tellmesh/uri2ops
COPY tellmesh/touri ./tellmesh/touri
COPY tellmesh/uri2voice ./tellmesh/uri2voice
COPY tellmesh/uri2pact ./tellmesh/uri2pact
COPY tellmesh/uri2run ./tellmesh/uri2run
COPY tellmesh/uri2verify ./tellmesh/uri2verify
COPY tellmesh/urigen ./tellmesh/urigen
COPY tellmesh/urish ./tellmesh/urish

RUN mkdir -p /app/www output/runtime/agents output/logs output/incidents output/proposals \
    && sed -i 's|../../tellmesh/|tellmesh/|g' pyproject.toml uv.lock

ENV UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-dev --extra server

ENV PYTHONUNBUFFERED=1
EXPOSE 8788

HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=5 \
  CMD curl -fsS http://127.0.0.1:8788/health >/dev/null || exit 1

CMD ["uvicorn", "agents.system.hypervisor_dashboard.main:app", "--host", "0.0.0.0", "--port", "8788"]
