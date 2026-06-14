# Example 14 — uri2ops serve daemon + remote registry (v0.5)

Start daemon:

```bash
python -m uri2ops.cli serve --host 127.0.0.1 --port 8791
```

Health and exported registry:

```bash
curl http://127.0.0.1:8791/health
curl http://127.0.0.1:8791/registry
curl http://127.0.0.1:8791/registry/sources
```

A2A agent card and task execution:

```bash
curl http://127.0.0.1:8791/.well-known/agent-card.json
curl -X POST http://127.0.0.1:8791/a2a/tasks \
  -H 'Content-Type: application/json' \
  -d '{"task": '"$(yq -o=json examples/10_browser_operator/task.health.yaml)"', "approve": true, "adapter": "mock"}'
```

MCP-style tool listing and invocation:

```bash
curl http://127.0.0.1:8791/mcp/tools
curl -X POST http://127.0.0.1:8791/mcp/tools/call \
  -H 'Content-Type: application/json' \
  -d '{"name":"browser_open","arguments":{"uri":"browser://chrome/page/open","payload":{"url":"http://localhost:8101/health"},"approve":true,"adapter":"mock"}}'
```

Remote registry merge:

```bash
python -m uri2ops.cli registry list
python -m uri2ops.cli registry validate
python -m uri2ops.cli operations describe browser wait
```

Local config: `config/operator_registry.uri.yaml` merges `config/extra_operator_registry.yaml` and can reference HTTP registries exported by another daemon (`http://127.0.0.1:8791/registry`).
