# Landing page — copy (PL)

Teksty na stronę sprzedażową. **URI i „control plane” tylko w sekcji technicznej**, nie w nagłówku.

## Hero

### Nagłówek

> **Automatyzacje i agenci AI przestali działać? Taskinity pokaże gdzie, dlaczego i co zrobić dalej.**

### Podtytuł

> Jeden chat i dashboard dla skryptów, webhooków, n8n, API, Dockera i agentów AI. Health, logi, incident, ticket i propozycja naprawy.

### CTA primary

> **Umów 10-min demo** · **Audyt automatyzacji od 2 500 zł**

### CTA secondary

> Zobacz jak działa na przykładzie faktur → błąd API → naprawa

---

## Sekcja: Problem (język klienta)

**Nagłówek:** Znasz to?

- n8n się wykonał, ale dane nie trafiły do systemu
- Nie wiesz, kto odpowiada za skrypt, który padł w nocy
- Szukasz po logach, webhookach i Excelu — 3 godziny na diagnozę
- Klient pyta „czy automatyzacja działa?” — a Ty nie masz jednego widoku

**Nagłówek:** Taskinity daje odpowiedź w minutach, nie godzinach.

---

## Sekcja: Co dostajesz

| Funkcja | Opis biznesowy |
|---------|----------------|
| **Jeden widok** | Wszystkie procesy: cron, API, Docker, n8n, agenci |
| **Chat** | „Co się stało z procesem faktur?” → status, przyczyna, logi |
| **Health** | Co działa, co nie — bez wchodzenia na 5 serwerów |
| **Incident** | Każdy błąd zapisany z kontekstem |
| **Ticket** | Eskalacja do naprawy lub zmiany w systemie |
| **Naprawa** | Propozycja kroków — najpierw podgląd, potem zatwierdzenie |

---

## Sekcja: Dla kogo

- **Software house’y** — panel procesów dla projektów i klientów
- **Integratorzy n8n / Make** — warstwa SLA i utrzymania wdrożeń
- **E-commerce** — zamówienia, faktury, ERP, marketplace
- **Biura i BPO** — dokumenty, OCR, KSeF, maile

---

## Sekcja: Oferta

| Pakiet | Cena | Czas |
|--------|------|------|
| Audyt automatyzacji | 2 500–5 000 zł | 1–3 dni |
| Pilot 3 procesów | 8 000–15 000 zł | 7–14 dni |
| Utrzymanie | 1 500–4 000 zł / mies. | ciągłe |

Szczegóły: [OFFERS.md](./OFFERS.md).

---

## Sekcja techniczna (niżej na stronie)

**Nagłówek:** Dla zespołów technicznych

> Pod spodem każdy proces jest **URI**. To samo URI można wykonać przez Web UI, API, CLI, workflow albo runtime (shell, HTTP, Docker, SSH).

> Taskinity to warstwa wykonania i naprawy nad agentami, workflow i narzędziami — zgodna z kierunkiem standardów MCP, A2A i `agent://` (IETF).

**Bullet points (tech):**

- `health://`, `repair://`, `ticket://`, `evolution://`
- Policy gate: dry-run przed mutacją
- Self-host, open pipeline
- Integracja z Langfuse / Phoenix do głębokiego tracingu LLM

---

## Social proof (placeholder)

- „Pilot 3 procesów — diagnoza z 2h do 15 min” (case study po pierwszym kliencie)
- Polski support i wdrożenie

---

## FAQ (skrót)

**Czy zastępujecie n8n?**  
Nie. Pokazujemy status i błędy procesów, które już macie.

**Czy to dla firm bez agentów AI?**  
Tak — skrypty, cron, webhooki i API też.

**Czy macie SOC2?**  
Nie — to produkt dla MŚP i software house’ów, self-host z policy gate.

**Czym różnicie się od LangSmith?**  
LangSmith świetny do trace LLM. My spinamy cały chaos automatyzacji — nie tylko LangChain.

---

Powiązane: [POSITIONING.md](./POSITIONING.md), [ASSESSMENT.md](./ASSESSMENT.md).
