# Taskinity — dokumentacja rynkowa

Materiały pozycjonowania, research konkurencji i go-to-market dla **Taskinity**.

Repo implementacyjne: [Resource Agent System](../README.md) (hypervisor monorepo).  
Taskinity to warstwa produktowa (chat, dashboard, API) nad modelem URI (`urish`, `hypervisor`, `uri2run`).

## Spis treści

| Dokument | Temat |
|----------|--------|
| **[ASSESSMENT.md](./ASSESSMENT.md)** | **Ocena strategiczna — kierunek dobry, research zaostrzony** |
| [POSITIONING.md](./POSITIONING.md) | Pozycjonowanie sprzedażowe vs techniczne |
| [PAIN_LANGUAGE.md](./PAIN_LANGUAGE.md) | Język bólu klienta — za co realnie płaci |
| [OFFERS.md](./OFFERS.md) | Oferty, cennik, wiadomości sprzedażowe |
| [LANDING_COPY.md](./LANDING_COPY.md) | Copy na landing page |
| [COMPETITIVE_LANDSCAPE.md](./COMPETITIVE_LANDSCAPE.md) | Mapa konkurencji |
| [MARKET_HYPOTHESIS.md](./MARKET_HYPOTHESIS.md) | ICP, segmentacja Polska, kto NIE |
| [STANDARDS.md](./STANDARDS.md) | `agent://`, MCP, A2A |
| [PRODUCT_READINESS.md](./PRODUCT_READINESS.md) | MVP scope, luki przed pilotem |
| [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) | Demo techniczne + sprzedażowe |
| [GTM_POLAND.md](./GTM_POLAND.md) | Plan 30/90 dni, integratorzy |
| [BATTLECARD.md](./BATTLECARD.md) | vs LangSmith Engine, n8n, Contro1 |

## Executive summary

**Kierunek produktu jest dobry:** Taskinity to warstwa sterowania (chat → API → CLI → runtime → observe → repair → ticket/evolution), nie kolejny framework agentów.

**Korekta sprzedażowa:** fraza „agent control plane” jest **zatłoczona** (Astrix, Fiddler, Contro1, Speakeasy, IBM = governance). Na pierwszym ekranie:

> **Taskinity — prosty command center dla automatyzacji i agentów. Co działa, co padło, dlaczego, jak naprawić.**

URI = przewaga demo i architektura pod spodem, nie hasło dla pierwszego klienta.

**Przewaga vs LangSmith Engine:** nie tylko repair agentów LangChain — **spinamy skrypty, cron, API, Docker, n8n, workflow i tickety jednym modelem URI**.

**Pierwszy rynek:** software house’y i **integratorzy n8n/Make** w Polsce (lokalne wdrożenie PL, pilot 5–15k zł).

Pełna analiza: **[ASSESSMENT.md](./ASSESSMENT.md)**.

## Powiązana dokumentacja techniczna

| Dokument | Po co |
|----------|--------|
| [docs/MENTAL_MODEL.md](../docs/MENTAL_MODEL.md) | 7 konceptów URI-first |
| [docs/AUTONOMY_LOOP.md](../docs/AUTONOMY_LOOP.md) | observe → repair → evolve |
| [docs/DASHBOARD.md](../docs/DASHBOARD.md) | Dashboard jako agent systemowy |
| [www/README.md](../www/README.md) | Chat UI |

## Status

| Dokument | Aktualizacja |
|----------|--------------|
| Całość `market/` | 2026-06-14 — research + ocena strategiczna |
