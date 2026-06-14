# Język bólu klienta — sprzedaż Taskinity

Klient **nie kupuje** „URI-first control plane”. Kupuje rozwiązanie konkretnego bólu o 9:00 w poniedziałek.

## Cytaty klienta (używaj w rozmowach i na landingu)

| Sytuacja | Co mówi klient |
|----------|----------------|
| Automatyzacja dokumentów | „Nie wiem, dlaczego automatyzacja faktur znowu nie działa.” |
| n8n / workflow | „n8n się wykonał, ale dane nie trafiły do systemu.” |
| Agenty AI | „Agent miał zrobić ticket, ale wysłał zły mail.” |
| Skrypty / cron | „Nie wiem, kto odpowiada za ten skrypt.” |
| Chaos integracji | „Nie mam jednego widoku automatyzacji, cronów, webhooków, API i agentów.” |
| E-commerce | „Zamówienia z Allegro nie weszły do ERP — gdzie to się urwało?” |
| Integrator | „Klient pisze ‘nie działa’, a my ręcznie sprawdzamy scenariusze, logi i API.” |
| Software house | „Mamy 12 projektów klientów — każdy ma inne webhooki i nikt nie widzi awarii centralnie.” |

## Mapowanie ból → funkcja Taskinity

| Ból | Odpowiedź Taskinity (język klienta) | Warstwa techniczna (nie na pierwszym slajdzie) |
|-----|-------------------------------------|------------------------------------------------|
| „Nie wiem co padło” | Jeden dashboard + chat: status procesu | `health://`, `view://process/...` |
| „Nie wiem dlaczego” | Przyczyna, ostatni błąd, logi | `log://`, `incident://` |
| „Kto ma naprawić?” | Ticket z incidentu | `ticket://bug/from-incident/...` |
| „Ile to kosztuje czasu?” | Raport pilota: czas diagnozy przed/po | artifact + metryki |
| „Czy mogę to naprawić bezpiecznie?” | Podgląd naprawy, potem zatwierdzenie | dry-run → `--approve` |
| „Mamy n8n i skrypty” | Nie zastępujemy — spinamy widok | URI nad http/shell/docker |

## Pytania discovery (30 rozmów)

```text
Jakie automatyzacje macie dziś w firmie?
Co najczęściej się psuje?
Gdzie szukacie logów?
Ile trwa ustalenie przyczyny?
Kto odpowiada za naprawę?
Czy klient widzi status procesu?
Czy płacilibyście za prosty dashboard health + ticket + repair?
Jakie 3 procesy warto byłoby podłączyć jako pierwsze?
```

## Efekt, za który klient płaci (nie architektura)

```text
wiem, co padło,
wiem, dlaczego,
mam ticket,
mam propozycję naprawy,
nie tracę 3 godzin na szukanie po logach.
```

## Antywzorce w pitchu

| Nie mów | Mów zamiast |
|---------|-------------|
| „URI-first control plane” | „Command center dla automatyzacji” |
| „Agentic ecosystem” | „Widok 3 procesów + chat” |
| „Zastępujemy n8n” | „Pokazujemy co z n8n i skryptów działa, a co padło” |
| „Konkurujemy z LangSmith” | „Spinamy skrypty, API, Docker i agentów — nie tylko LangChain” |

Powiązane: [ASSESSMENT.md](./ASSESSMENT.md), [POSITIONING.md](./POSITIONING.md), [OFFERS.md](./OFFERS.md).
