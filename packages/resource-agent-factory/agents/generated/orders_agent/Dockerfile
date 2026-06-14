# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: /home/tom/github/wronai/hypervisor/contracts/agents/test_orders_agent.yaml
# Contract hash: sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -e .
EXPOSE 8101
CMD ["uvicorn", "agents.generated.orders_agent.main:app", "--host", "0.0.0.0", "--port", "8101"]