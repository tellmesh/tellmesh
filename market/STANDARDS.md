# Standardy: agent://, MCP, A2A

Pozycjonowanie Taskinity względem prac standardyzacyjnych i protokołów interoperacyjności (stan: 2026-06).

## Stos protokołów (jak to widzi rynek)

```text
┌─────────────────────────────────────────┐
│  Taskinity — operational control plane   │
│  repair:// ticket:// evolution:// view:// │
└──────────────────┬──────────────────────┘
                   │ wykorzystuje
┌──────────────────▼──────────────────────┐
│  agent://  MCP  A2A  (addressing + comm) │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  HTTP / WSS / gRPC / Docker / SSH        │
└─────────────────────────────────────────┘
```

Taskinity **nie zastępuje** warstwy protokołów — dodaje **operational URI** nad nimi.

## IETF draft-narvaneni-agent-uri-03

**Źródło:** [datatracker.ietf.org](https://datatracker.ietf.org/doc/html/draft-narvaneni-agent-uri-03)

### Co definiuje

- Schemat `agent://` jako **addressing i discovery** agentów
- 4 poziomy conformance (Level 0–3):
  - **L0:** `agent+https://` — bezpośrednie wywołanie
  - **L1:** `/.well-known/agents.json` — discovery
  - **L2:** resolution, caching, multi-transport
  - **L3:** deskryptory, auth, wersjonowanie
- Uzupełnia MCP, A2A, ACP — „warstwa adresowania, której im brakuje”

### Implikacja dla Taskinity

| Aspekt | Działanie |
|--------|-----------|
| Komunikat | „Zgodni z kierunkiem IETF, operational layer ponad agent://” |
| Ryzyko | IETF może ustalić canonical format — unikać własnego dialektu |
| Roadmap | Conformance Level 1–2: `/.well-known/agents.json`, agent card |

### Mapowanie na implementację w repo

| Wymaganie draft | Taskinity / hypervisor | Status |
|-----------------|------------------------|--------|
| `agent://` identity | `agent://weather-map-agent`, `agent://hypervisor-dashboard` | ✅ |
| Agent descriptor | `/.well-known/agent-card.json` | ✅ częściowo |
| Multi-transport | uri2run: http, docker, ssh, mcp, a2a | ✅ |
| `/.well-known/agents.json` registry | brak centralnego rejestru domeny | ⚠️ TODO |
| Resolution / caching | uri3 scan, touri matching | ⚠️ częściowo |

## Równoległe prace IETF

| Draft / praca | Zakres | Relacja do Taskinity |
|---------------|--------|---------------------|
| **ARDP** (Agent Registration & Discovery) | Control plane discovery, MCP/A2A/HTTP/gRPC | Konkurencja na discovery, nie execution |
| **CATALIST gap analysis** (IETF 125) | Identity, discovery, session, transport | Trend „Internet of Agents” |
| **arXiv 2601.14567** + **Govcraft/agent-uri-rs** | Topology-independent identity, DHT | Potencjalny komponent OSS |

## MCP (Model Context Protocol)

### W Taskinity

| Powierzchnia | Endpoint / transport | Plik |
|--------------|---------------------|------|
| uri2ops serve | `GET /mcp/tools`, `POST /mcp/tools/call` | `packages/uri2ops/uri2ops/server/routes/mcp.py` |
| uri2run client | `mcp://host:port` → HTTP bridge | `packages/uri2run/uri2run/transports/mcp_transport.py` |
| hypervisor-dashboard :8788 | **brak** `/mcp/*` | — |

### Uwaga produktowa

MCP w Taskinity to **HTTP wrapper**, nie stdio MCP server. Klienci Cursor/IDE wymagają mostka HTTP lub osobnego adaptera stdio.

## A2A (Agent-to-Agent)

### W Taskinity

| Powierzchnia | Endpoint | Plik |
|--------------|----------|------|
| uri2ops serve | `GET /.well-known/agent-card.json`, `POST /a2a/tasks` | `packages/uri2ops/uri2ops/server/routes/a2a.py` |
| uri2run client | `a2a://host:port` | `packages/uri2run/uri2run/transports/a2a_transport.py` |
| hypervisor-dashboard :8788 | agent-card only, **brak** `/a2a/tasks` | `hypervisor_dashboard_agent/routes.py` |
| Wygenerowani agenci :8101 | agent-card + REST | domains/* |

## Tabela dostępności protokołów

| Warstwa | MCP | A2A | Port | Uwagi |
|---------|-----|-----|------|-------|
| **uri2ops serve** | ✅ | ✅ | 8791 | Główny punkt protokołów |
| **hypervisor-dashboard** | ❌ | ⚠️ card only | 8788 | REST: `/api/ask`, `/api/uri/call` |
| **Wygenerowani agenci** | ❌ | ⚠️ partial | 8101 | `/health`, `/commands` |
| **uri2run (klient)** | ✅ | ✅ | — | Transport do zdalnych serwerów |

## Komunikat marketingowy vs standardy

**Poprawnie:**

> Taskinity stoi warstwę wyżej niż MCP/A2A i agent:// — wykorzystuje te protokoły, ale wystawia zespołom wspólny język URI do sterowania, obserwacji i naprawy procesów.

**Niepoprawnie:**

> Taskinity definiuje standard agent:// dla branży.

## Rekomendacje conformance (roadmap)

1. **Level 1:** publikować `/.well-known/agents.json` na dashboard i deploymentach
2. **Level 2:** uri3 scan jako resolution z cache
3. **Operational URI registry:** udokumentować schematy `repair://`, `ticket://`, `evolution://` jako rozszerzenie ponad draft (nie konflikt)
4. **MCP stdio adapter:** opcjonalny mostek dla Cursor IDE
5. **Dashboard `/a2a/tasks`:** spójność z uri2ops dla operatorów

## Referencje

- [draft-narvaneni-agent-uri-03](https://datatracker.ietf.org/doc/html/draft-narvaneni-agent-uri-03)
- [ARDP draft](https://www.ietf.org/archive/id/draft-pioli-agent-discovery-00.html)
- [Govcraft/agent-uri-rs](https://github.com/Govcraft/agent-uri-rs)
- [docs/STANDARDS.md](../docs/STANDARDS.md) — implementacja w repo
