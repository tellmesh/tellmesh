# Example 03 — remote agent host przez Docker + SSH

Kontener udaje zewnętrzną maszynę do testów wdrożeń i skanowania.

## Start

```bash
make docker-ssh-up
# lub
docker compose -f examples/03_ssh_remote_agent/docker-compose.yml up --build -d
```

Kontener wystawia:

```txt
SSH:        ssh://deploy@localhost:2222/opt/agents   (hasło: deploy)
HTTP mock:  http://localhost:8101
Agent Card: http://localhost:8101/.well-known/agent-card.json
Health:     http://localhost:8101/health
```

> Jeśli port `8101` jest zajęty na hoście, zmapuj inny port w `docker-compose.yml` lub zatrzymaj konfliktującą usługę.

## Test SSH

```bash
ssh -p 2222 deploy@localhost 'ls -la /opt/agents'
```

## Skanowanie HTTP przez uri3

```bash
make scan-http
# lub
uri3 scan http://localhost:8101
```

## Skanowanie SSH

```bash
uri3 scan ssh://deploy@localhost:2222/opt/agents
```

> **Stan implementacji:** skaner `ssh://` w `uri3` nie jest jeszcze zaimplementowany (polecenie zwraca pustą listę). Ręczny test SSH działa; pełna automatyzacja wymaga kluczy SSH i przyszłego `uri3.scanner.ssh_scanner`.

## Stop

```bash
make docker-ssh-down
```
