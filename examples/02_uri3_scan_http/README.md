# Example 02 — skanowanie HTTP/A2A-like

Ten przykład zakłada działający agent HTTP — np. mock z [`../03_ssh_remote_agent/`](../03_ssh_remote_agent/) albo `make run-user-agent`.

```bash
make scan-http
# lub
uri3 scan http://localhost:8101
```

Sprawdzane endpointy:

```txt
/health
/capabilities
/.well-known/agent-card.json
/.well-known/agent.json
```

To jest w paczce `uri3`. Hypervisor później interpretuje wyniki skanowania (registry, lifecycle).

Powiązane:

```bash
uri3 schema 'http://'
uri3 resolve http://localhost:8101/health
```
