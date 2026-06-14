# Hipoteza rynkowa (zaostrzona)

Po [ASSESSMENT.md](./ASSESSMENT.md) — ICP z cenami, kanałami i segmentami wykluczonymi.

## Teza (sprzedażowa)

**Nie sprzedawaj platformy agentowej. Sprzedawaj kontrolę nad chaosem automatyzacji.**

Technicznie: URI-first operational layer.  
Klient kupuje: wiem co padło, dlaczego, mam ticket i propozycję naprawy — bez 3h w logach.

---

## Dlaczego Polska first

| Fakt | Źródło | Implikacja |
|------|--------|------------|
| Gospodarka cyfrowa ~44 mld USD | [Trade.gov](https://www.trade.gov/country-commercial-guides/poland-digital-economy) | Popyt na automatyzację |
| **90% firm IT to MŚP** | Trade.gov | Enterprise CP za drogie |
| **1300+ software dev companies** | [PAIH / trade.gov.pl](https://www.trade.gov.pl/en/news/the-information-communication-technology-sector-a-paih-report/) | Duży prospecting pool |
| Wymóg wsparcia PL | Trade.gov | Lokalne wdrożenie = przewaga |
| E-commerce ~26,7 mld USD (2026) | [Mordor Intelligence](https://www.mordorintelligence.com/industry-reports/poland-ecommerce-market) | Segment operacyjny |
| MŚP wdrażają AI (finanse, obsługa) | [SAIO](https://www.saio.com/newsroom/news/nie-tylko-korporacje-polskie-msp-coraz-chetniej-wdrazaja-ai) | BPO / księgowość |

---

## ICP — priorytety sprzedaży

### Priorytet 1: Software house 10–80 osób

| | |
|---|---|
| **Buyer** | Właściciel, CTO, Head of Delivery, Tech Lead |
| **Ból** | Wiele projektów, webhooków, cronów, CI, n8n — brak jednego widoku awarii |
| **Sprzedaż** | „Panel kontroli procesów dla projektów i klientów” |
| **Dlaczego kupią** | Wewnętrznie + odsprzedaż klientom jako utrzymanie |
| **Pilot** | 8 000–15 000 zł netto |
| **Wejście** | 3 procesy: GitHub Action + webhook/API + skrypt/cron |

### Priorytet 2: Integratorzy n8n / Make / Power Automate

| | |
|---|---|
| **Buyer** | Właściciel firmy automatyzacyjnej, consultant |
| **Ból** | Klient: „nie działa” → ręczne sprawdzanie scenariuszy, logów, API |
| **Sprzedaż** | „Warstwa utrzymania i SLA dla automatyzacji” |
| **Dlaczego kupią** | Dodatek do oferty monitoring/maintenance |
| **Pilot** | 5 000–12 000 zł netto |
| **Po pilocie** | Abonament **1 500–4 000 zł/mies.** |

**Kanał #1** — jeden dobry integrator > pięciu końcowych klientów.

### Priorytet 3: E-commerce 20–200 osób

| | |
|---|---|
| **Buyer** | Właściciel, COO, Head of E-commerce, IT Manager |
| **Ból** | Sklep–ERP–magazyn–kurier–Allegro–faktury–zwroty |
| **Sprzedaż** | „Centrum kontroli zamówień i integracji” |
| **Demo** | „Status procesu zamówień z Allegro” → API OK, ERP opóźnia, ticket |
| **Pilot** | 10 000–20 000 zł netto |

### Priorytet 4: Biura rachunkowe / BPO dokumentowe

| | |
|---|---|
| **Buyer** | Właściciel, dyrektor operacyjny |
| **Ból** | Maile, OCR, KSeF, różne formaty, proces się zacina |
| **Sprzedaż** | „Widok procesu dokumentu od maila do systemu księgowego” |
| **Pilot** | 7 000–15 000 zł netto |

### Priorytet 5: Produkcja / logistyka MŚP

| | |
|---|---|
| **Buyer** | Dyrektor operacyjny, IT manager, właściciel |
| **Ból** | ERP, WMS, CSV, importy, etykiety, raporty |
| **Sprzedaż** | „Monitor importów/eksportów i zadań automatycznych” |
| **Pilot** | 10 000–25 000 zł netto (integracje terenowe) |

---

## Komu NIE sprzedawać na początku

| Segment | Dlaczego nie |
|---------|--------------|
| Administracja publiczna | Długi procurement |
| Banki, ubezpieczalnie | Compliance, GRC, SIEM |
| Duże enterprise | Astrix/Contro1/IBM już tam |
| Sektory mocno regulowane | EU AI Act governance — popyt rośnie ([AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)), cykl sprzedaży za długi |
| Mikrofirmy bez automatyzacji | Brak bólu — najpierw trzeba zbudować procesy |

---

## Pierwszych 10 klientów — miks

```text
4  software house / DevOps / AI automation
2  integratorów n8n / Make / Power Automate
2  e-commerce (magazyn / ERP)
1  biuro rachunkowe / BPO
1  produkcja / logistyka (import/eksport danych)
```

---

## MVP produktowy (jeden problem)

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

Integracje MVP (3, nie 15): `http`/webhook, `shell`/cron, `docker`.  
Reszta później: n8n, GitHub Actions, ssh, mcp, jira.

Szczegóły: [PRODUCT_READINESS.md](./PRODUCT_READINESS.md).

---

## Ryzyka (zaktualizowane)

| Ryzyko | Mitigacja |
|--------|-----------|
| Zatłoczona kategoria „control plane” | Command center, nie CP na pierwszym ekranie |
| LangSmith Engine | Przewaga: wszystkie procesy, nie tylko LangChain |
| Brak języka bólu | [PAIN_LANGUAGE.md](./PAIN_LANGUAGE.md) |
| Brak kanału integratorów | Priorytet #2 ICP, oferta SLA |
| URI tylko na papierze | `urish proof` + demo sprzedażowe |

---

## Metryki pilota

| Metryka | Cel |
|---------|-----|
| Czas diagnozy (przed/po) | −50% self-report |
| 3 procesy pod URI | 7–14 dni |
| Proof chat = CLI = API | 1 scenariusz nagrany |
| Konwersja pilot → retainer | ≥ 1/3 integratorów |

Oferty: [OFFERS.md](./OFFERS.md).
