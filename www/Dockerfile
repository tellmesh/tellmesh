# www chat — hypervisor-dashboard-agent + static UI
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./
COPY packages ./packages
COPY agents ./agents
COPY contracts ./contracts
COPY schemas ./schemas
COPY deployments ./deployments
COPY config ./config
COPY domains ./domains
COPY knowledge ./knowledge
COPY examples ./examples

RUN mkdir -p /app/www output/runtime/agents output/logs output/incidents output/proposals

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
