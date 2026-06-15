# Gotowość produktu vs obietnica rynkowa

Walidacja implementacji TellMesh / Taskinity względem tezy URI-first control plane (stan kodu: v0.5.22+, 2026-06-14).

## Podsumowanie

| Obszar | Gotowość | Uwagi |
|--------|----------|-------|
| Architektura URI-first | ✅ Silna | Schematy, policy, multi-surface |
| Demo E2E dla klienta | ⚠️ Wymaga domknięcia | Docker, wersje, MCP w `make start` |
| Observability (trace/cost) | ⚠️ Słaba | Lokalne logi/health, brak Langfuse-level |
| Enterprise governance | ⚠️ Podstawowa | Policy gate, nie SOC2/multi-tenant |

**Wniosek:** Sprzedawaj **health + incident + ticket + repair dla 3 procesów**, nie „pełny ekosystem agentów”.

## MVP scope (jeden problem)

> **Agent/Automation Health + Repair Dashboard**

```text
1. Rejestr procesów jako URI
2. Health check dla każdego URI
3. Ostatnie wykonania i błędy
4. Chat: „co się stało z procesem X?”
5. Incident z błędu
6. Ticket z incidentu
7. Proposal naprawy
8. Proof: to samo URI — chat, API, CLI
```

### Integracje MVP (3, nie 15)

**Teraz:**

```text
http:// / webhook / REST API
shell:// / local script / cron
docker:// / container health
```

**Potem:** n8n, GitHub Actions, ssh, mcp, a2a, jira, slack/teams.

### Roadmap: `urish proof`

Komenda jednego proof dla wszystkich warstw — [DEMO_SCRIPT.md](./DEMO_SCRIPT.md). Status: **TODO** przed pierwszą sprzedażą masową.

---

## Podsumowanie gotowości

## Co już działa (dowód implementacji)

### URI schemes (control plane)

| Scheme | Rola | Kod / docs |
|--------|------|------------|
| `agent://` | Tożsamość agenta | `domains/*/uri_tree.yaml` |
| `repair://` | diagnose / apply | `hypervisor/repair/supervisor.py` |
| `ticket://` | Planfile → artifact | `hypervisor/integrations/planfile/ticket_mapper.py` |
| `evolution://` | proposal from ticket/incident | `uri3/artifacts/evolution_source.py` |
| `incident://` | Failure artifact | `docs/AUTONOMY_LOOP.md` |
| `view://` | UI render targets | `hypervisor_dashboard_agent/uri_client.py` |
| `health://`, `runtime://`, `log://` | Obserwacja | `docs/URI_COOKBOOK.md` |

### Multi-surface execution

| Powierzchnia | Wejście | Status |
|--------------|---------|--------|
| CLI | `urish call`, `repair`, `ticket`, `evolve` | ✅ |
| REST API | `POST /api/uri/call`, `/api/ask` | ✅ |
| Chat UI | `www/` → dashboard agent :8788 | ✅ |
| Runtime | uri2run: shell, http, docker, ssh, mcp, a2a | ✅ |
| MCP/A2A server | `uri2ops serve :8791` | ✅ (osobny proces) |

### Pętle operacyjne

```text
observe → diagnose → repair → incident → evolve → ticket
```

Zaimplementowane w: `docs/AUTONOMY_LOOP.md`, `hypervisor/repair/supervisor.py`, `urish/backends/evolve.py`.

### Policy gate

- `--dry-run` / `--approve` / `--sandbox`
- Klasyfikacja read vs mutation w `urish/policy.py`

## Luki przed pierwszym pilotem (krytyczne)

### 1. Docker chat bez `agents/generated/`

**Objaw:** `POST /api/uri/call` → 500 przy repair weather agenta.

```
FileNotFoundError: Generated agent path not found: /app/agents/generated/weather_map_agent
```

**Przyczyna:** `www/docker-compose.yml` montuje tylko `www/` i `deployments/`, nie `agents/generated/`.

**Fix:** dodać volume `../agents/generated:/app/agents/generated:ro` lub graceful error w UI.

### 2. Błąd 500 zamiast czytelnego envelope

UI powinno dostać `ServiceResult` z komunikatem „agent nie istnieje w kontenerze” + sugestia `uri ecosystem generate`.

### 3. `make start` bez uri2ops

MCP/A2A wymagają osobnego `uri2ops serve --port 8791` — brak w domyślnym starcie.

### 4. Wersja w health vs repo

Health zwraca `version: 0.1.0`, repo `0.5.22+` — mylące przy debugowaniu i demo.

## Luki ważne (UX / operacje)

| Luka | Wpływ | Priorytet |
|------|-------|-----------|
| Dashboard bez `POST /a2a/tasks` | Niespójność z uri2ops | P1 |
| Brak streaming w `/api/ask` | Timeout na długich planach LLM | P2 |
| Orphan containers przy `make stop` | Bałagan dev | P2 |
| Brak trace/cost observability | Słabsza odpowiedź vs Langfuse | P2 |
| MCP stdio (Cursor native) | Wymaga HTTP bridge | P2 |

## Macierz: obietnica demo vs stan

| Krok demo | Obietnica | Stan |
|-----------|----------|------|
| NL → plan URI w chacie | ✅ | Działa |
| Ten sam URI w CLI | ✅ | Działa |
| Ten sam URI w API | ✅ | Działa |
| Repair z chatu (Docker) | ✅ | ❌ bez volume |
| incident → evolution | ✅ | Działa z hosta |
| MCP/A2A out of the box | ⚠️ | Wymaga uri2ops serve |
| Golden path 15 min | ✅ | `examples/30_golden_path/` |

## Checklist przed pilotem (8–12 tys. zł)

- [ ] Volume `agents/generated` w docker-compose
- [ ] Graceful errors w `/api/uri/call`
- [ ] Opcjonalny `make start-mcp` lub dokumentacja uri2ops w README pilota
- [ ] Ujednolicenie wersji w health / agent-card
- [ ] Nagranie demo 8 min ([DEMO_SCRIPT.md](./DEMO_SCRIPT.md))
- [ ] Smoke test: chat → repair dry-run → approve (na hosta lub pełny Docker)
- [ ] **`urish proof`** — proof wszystkich warstw w 30 s

## Roadmap alignment

Powiązane pozycje z [docs/ROADMAP.md](../docs/ROADMAP.md) i [TODO.md](../TODO.md):

- `health://agent/{deployment}` — explicit scheme alias
- `repair://agent/{deployment}/auto` — TODO w repo
- Dashboard A2A endpoint
- Integracja OTel / Langfuse jako read URI

## Jak mówić o gotowości klientowi

**Uczciwie (język klienta):**

> „W 7–14 dni podłączamy 3 wasze procesy — faktury, webhook, cron — i pokazujemy w chacie: co działa, co padło, dlaczego i co naprawić.”

**Unikać:**

> „Pełna platforma enterprise z SOC2 i trace’ami jak LangSmith.”
