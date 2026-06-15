# www chat — hypervisor-dashboard-agent + static UI
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY tellmesh/tellmesh/pyproject.toml tellmesh/tellmesh/uv.lock tellmesh/tellmesh/README.md ./
COPY tellmesh/tellmesh/contracts ./contracts
COPY tellmesh/tellmesh/schemas ./schemas
COPY tellmesh/tellmesh/deployments ./deployments
COPY tellmesh/tellmesh/config ./config
COPY tellmesh/tellmesh/domains ./domains
COPY tellmesh/tellmesh/knowledge ./knowledge
COPY tellmesh/tellmesh/examples ./examples
COPY tellmesh/tellmesh/agents ./agents

# TellMesh editable path deps (patched to tellmesh/* before uv sync)
COPY tellmesh/hypervisor ./tellmesh/hypervisor
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
    && sed -i 's|path = "../|path = "tellmesh/|g' pyproject.toml uv.lock

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
