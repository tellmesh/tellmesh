window.__INTEGRATIONS_I18N__ = {
  "cards": {
    "wordpress-connector": {
      "pl": {
        "tag": "WordPress",
        "title": "Lead z formularza do CRM",
        "lead": "Hook formularza lub REST API wysyła zdarzenie do Taskinity, a agent dopisuje kontakt w CRM i odsyła potwierdzenie."
      },
      "en": {
        "tag": "WordPress",
        "title": "Form lead to CRM",
        "lead": "Form hook or REST API sends an event to Taskinity; the agent adds the contact in CRM and sends confirmation."
      },
      "de": {
        "tag": "WordPress",
        "title": "Formular-Lead ins CRM",
        "lead": "Form-Hook oder REST-API sendet Event an Taskinity; Agent trägt Kontakt ins CRM ein."
      }
    },
    "wordpress-card": {
      "pl": {
        "tag": "WordPress",
        "title": "WP · formularze · REST"
      },
      "en": {
        "tag": "WordPress",
        "title": "WP · forms · REST"
      },
      "de": {
        "tag": "WordPress",
        "title": "WP · Formulare · REST"
      }
    },
    "erp-connector": {
      "pl": {
        "tag": "ERP · CRM",
        "title": "Comarch, Subiekt, HubSpot, Salesforce",
        "lead": "REST, SOAP, CSV, SQL albo okna Windows. System rozdziela automatyczne kroki od tych, które wymagają akceptacji człowieka."
      },
      "en": {
        "tag": "ERP · CRM",
        "title": "Comarch, Subiekt, HubSpot, Salesforce",
        "lead": "REST, SOAP, CSV, SQL or Windows UI. Automatic steps vs human approval are separated."
      },
      "de": {
        "tag": "ERP · CRM",
        "title": "Comarch, Subiekt, HubSpot, Salesforce",
        "lead": "REST, SOAP, CSV, SQL oder Windows-UI — automatische vs manuelle Schritte getrennt."
      }
    },
    "erp-card": {
      "pl": {
        "tag": "ERP · CRM",
        "title": "Comarch · Subiekt · Salesforce · HubSpot"
      },
      "en": {
        "tag": "ERP · CRM",
        "title": "Comarch · Subiekt · Salesforce · HubSpot"
      },
      "de": {
        "tag": "ERP · CRM",
        "title": "Comarch · Subiekt · Salesforce · HubSpot"
      }
    },
    "woocommerce-connector": {
      "pl": {
        "tag": "WooCommerce",
        "title": "Zamówienie do faktury i magazynu",
        "lead": "Webhook sklepu uruchamia workflow — pobierz zamówienie, sprawdź płatność, wystaw fakturę i zsynchronizuj stan."
      },
      "en": {
        "tag": "WooCommerce",
        "title": "Order to invoice and inventory",
        "lead": "Store webhook runs a workflow — fetch order, verify payment, issue invoice and sync stock."
      },
      "de": {
        "tag": "WooCommerce",
        "title": "Bestellung zu Rechnung und Lager",
        "lead": "Shop-Webhook startet Workflow — Bestellung holen, Zahlung prüfen, Rechnung und Bestand syncen."
      }
    },
    "baselinker-connector": {
      "pl": {
        "tag": "BaseLinker",
        "title": "Marketplace hub bez ślepych cronów",
        "lead": "Cron lub n8n woła API BaseLinker, a Taskinity porównuje zamówienia, stany i błędy synchronizacji z ERP."
      },
      "en": {
        "tag": "BaseLinker",
        "title": "Marketplace hub without blind crons",
        "lead": "Cron or n8n calls BaseLinker API; Taskinity compares orders, stock and sync errors with ERP."
      },
      "de": {
        "tag": "BaseLinker",
        "title": "Marketplace-Hub ohne blinde Cronjobs",
        "lead": "Cron oder n8n ruft BaseLinker-API; Taskinity vergleicht Bestellungen, Bestand und Sync-Fehler mit ERP."
      }
    },
    "allegro-connector": {
      "pl": {
        "tag": "Allegro.pl",
        "title": "OAuth, zamówienia, zwroty",
        "lead": "Agent pilnuje tokenu OAuth, pobiera checkout forms, wykrywa 429/503 i pokazuje w chacie, które zamówienie utknęło."
      },
      "en": {
        "tag": "Allegro.pl",
        "title": "OAuth, orders, returns",
        "lead": "Agent manages OAuth token, fetches checkout forms, detects 429/503 and shows stuck orders in chat."
      },
      "de": {
        "tag": "Allegro.pl",
        "title": "OAuth, Bestellungen, Retouren",
        "lead": "Agent verwaltet OAuth-Token, lädt Checkout Forms, erkennt 429/503 und zeigt hängende Bestellungen im Chat."
      }
    },
    "woocommerce-card": {
      "pl": {
        "tag": "WooCommerce",
        "title": "Sklep · zamówienia · stany"
      },
      "en": {
        "tag": "WooCommerce",
        "title": "Store · orders · stock"
      },
      "de": {
        "tag": "WooCommerce",
        "title": "Shop · Bestellungen · Bestand"
      }
    },
    "baselinker-card": {
      "pl": {
        "tag": "Baselinker",
        "title": "Magazyn · marketplace hub"
      },
      "en": {
        "tag": "BaseLinker",
        "title": "Warehouse · marketplace hub"
      },
      "de": {
        "tag": "BaseLinker",
        "title": "Lager · Marketplace-Hub"
      }
    },
    "allegro-card": {
      "pl": {
        "tag": "Allegro.pl",
        "title": "Aukcje · zamówienia · OAuth"
      },
      "en": {
        "tag": "Allegro.pl",
        "title": "Auctions · orders · OAuth"
      },
      "de": {
        "tag": "Allegro.pl",
        "title": "Auktionen · Bestellungen · OAuth"
      }
    },
    "ecommerce-spotlight": {
      "en": {
        "title": "Example: WooCommerce → BaseLinker → ERP (one view)",
        "cta_label": "Try a question in chat",
        "cta_hint": "The 3-process pilot covers exactly this layout.",
        "body": "Typical e-commerce pilot — three systems, one chat on failure:\n\n```\n1. WooCommerce webhook  →  workflow://order/new\n2. BaseLinker sync      →  shell://scripts/sync-baselinker.sh\n3. ERP invoice          →  http://erp.local/api/invoices  (agent invoices-agent.local)\n4. Taskinity            →  health every 5 min + webhook alert + NL chat\n\n# when something breaks:\n\"Diagnose Allegro sync and show latest ERP errors\"\n→ repair://agent/invoices-agent.local/diagnose\n```\n\n- Webhook `order.created` / `order.updated` → invoice or warehouse agent.\n- Health on Woo REST endpoint — see immediately if sync is stuck.\n- Chat: “why did order #4521 not reach BaseLinker?”\n\n- BaseLinker API (`getOrders`, `updateInventory`) as a workflow URI step.\n- Cron every N minutes + order count vs WooCommerce / Allegro.\n\n- Agent with Allegro OAuth token — orders, shipping status, returns.\n- On 429/503: supervisor retry with backoff, incident instead of silent fail.\n"
      },
      "pl": {
        "title": "Przykład: WooCommerce → Baselinker → ERP (jeden widok)",
        "cta_label": "Wypróbuj pytanie w chacie",
        "cta_hint": "Pilot 3 procesów obejmuje właśnie taki układ.",
        "body": "Typowy pilot e-commerce — trzy systemy, jeden chat przy awarii:\n\n```\n1. WooCommerce webhook  →  workflow://order/new\n2. Baselinker sync      →  shell://scripts/sync-baselinker.sh\n3. ERP faktura          →  http://erp.local/api/invoices  (agent invoices-agent.local)\n4. Taskinity            →  health co 5 min + webhook alert + chat NL\n\n# gdy coś padnie:\n\"Zdiagnozuj synchronizację Allegro i pokaż ostatnie błędy ERP\"\n→ repair://agent/invoices-agent.local/diagnose\n```\n\n- Webhook `order.created` / `order.updated` → agent faktur lub magazynu.\n- Health na endpoint Woo REST — widać od razu, czy synchronizacja stoi.\n- Chat: „dlaczego zamówienie #4521 nie poszło do Baselinkera?”\n\n- API Baselinker (`getOrders`, `updateInventory`) jako krok workflow URI.\n- Cron co N minut + porównanie liczby zamówień vs WooCommerce / Allegro.\n\n- Agent z tokenem OAuth Allegro — pobieranie zamówień, status wysyłki, zwroty.\n- Przy 429/503: supervisor retry z backoff, incident zamiast cichego failu.\n"
      },
      "de": {
        "title": "Beispiel: WooCommerce → BaseLinker → ERP (eine Ansicht)",
        "cta_label": "Frage im Chat testen",
        "cta_hint": "Der 3-Prozess-Pilot deckt genau dieses Layout ab.",
        "body": "Typischer E-Commerce-Pilot — drei Systeme, ein Chat bei Ausfall:\n\n```\n1. WooCommerce Webhook  →  workflow://order/new\n2. BaseLinker Sync      →  shell://scripts/sync-baselinker.sh\n3. ERP Rechnung         →  http://erp.local/api/invoices  (Agent invoices-agent.local)\n4. Taskinity            →  Health alle 5 Min + Webhook + NL-Chat\n\n# bei Ausfall:\n\"Allegro-Sync diagnostizieren und letzte ERP-Fehler zeigen\"\n→ repair://agent/invoices-agent.local/diagnose\n```\n\n- Webhook `order.created` / `order.updated` → Rechnungs- oder Lager-Agent.\n- Health auf Woo-REST — sofort sichtbar, ob Sync hängt.\n- Chat: „warum ging Bestellung #4521 nicht zu BaseLinker?”\n\n- BaseLinker API (`getOrders`, `updateInventory`) als Workflow-URI-Schritt.\n- Cron alle N Minuten + Bestellvergleich WooCommerce / Allegro.\n\n- Agent mit Allegro-OAuth — Bestellungen, Versandstatus, Retouren.\n- Bei 429/503: Supervisor-Retry mit Backoff, Incident statt stillem Fail."
      }
    },
    "portal-connector": {
      "pl": {
        "tag": "Strony i portale",
        "title": "Logowanie, pobieranie danych, formularze",
        "lead": "Playwright lub browser adapter wykonuje czynności w portalu, robi screenshot i zatrzymuje się przed wysyłką danych."
      },
      "en": {
        "tag": "Websites & portals",
        "title": "Login, data fetch, forms",
        "lead": "Playwright or browser adapter acts in the portal, captures a screenshot and stops before submitting data."
      },
      "de": {
        "tag": "Webseiten & Portale",
        "title": "Login, Datenabruf, Formulare",
        "lead": "Playwright oder Browser-Adapter arbeitet im Portal, Screenshot und Stopp vor dem Absenden."
      }
    },
    "portal-card": {
      "pl": {
        "tag": "Portale · WWW",
        "title": "Portal dostawcy · raport CSV"
      },
      "en": {
        "tag": "Portals · WWW",
        "title": "Supplier portal · CSV report"
      },
      "de": {
        "tag": "Portale · WWW",
        "title": "Lieferantenportal · CSV-Bericht"
      }
    },
    "api-sites-card": {
      "pl": {
        "tag": "Strony · API",
        "title": "Inne strony i systemy"
      },
      "en": {
        "tag": "Sites · API",
        "title": "Other sites and systems"
      },
      "de": {
        "tag": "Seiten · API",
        "title": "Andere Seiten und Systeme"
      }
    },
    "screenshot-schedule-connector": {
      "pl": {
        "tag": "Screenshot · monitor",
        "title": "Harmonogram rzutów ekranu stron",
        "lead": "Chat rozpoznaje prompt NL i planuje stabilny workflow URI — dry-run, approve, opcjonalnie Playwright i cron na hoście."
      },
      "en": {
        "tag": "Screenshot · monitor",
        "title": "Website screenshot schedule",
        "lead": "Chat detects NL prompts and plans a stable workflow URI — dry-run, approve, optional Playwright and host cron."
      },
      "de": {
        "tag": "Screenshot · Monitor",
        "title": "Website-Screenshot-Zeitplan",
        "lead": "Chat erkennt NL-Prompts und plant eine stabile Workflow-URI — Dry-run, Approve, optional Playwright und Host-Cron."
      }
    },
    "screenshot-schedule-card": {
      "pl": {
        "tag": "Chat · workflow",
        "title": "Stabilny URI z batch demo"
      },
      "en": {
        "tag": "Chat · workflow",
        "title": "Stable URI from batch demo"
      },
      "de": {
        "tag": "Chat · Workflow",
        "title": "Stabile URI aus Batch-Demo"
      }
    },
    "screenshot-spotlight": {
      "pl": {
        "title": "Przykład: harmonogram screenshotów z chatu (stabilny URI)",
        "cta_label": "Wypróbuj pytanie w chacie",
        "cta_hint": "Trzecia linia z batch demo Taskinity Chat planuje ten workflow.",
        "body": "Typowy pilot monitorowania stron — chat NL, stabilny workflow, opcjonalny cron:\n\n```\n1. Chat NL (batch)     →  workflow://graph/website-screenshot-schedule/dry-run\n2. Dry-run / approve   →  mock browser lub Playwright → ~/images/\n3. Host cron (opcja)   →  cron://www/monitor/landing + install-cron.sh\n4. Taskinity           →  health co 5 min + logi + chat przy awarii\n```\n\n- Prompt „rob rzuty ekranów…” **nie** tworzy losowego `domain://` — zawsze ten sam workflow ID.\n- `bash examples/35_website_screenshot_schedule/run.sh` — PASS w CI.\n- Po edycji: `make www-docs` i restart kontenera WWW (Docker).\n"
      },
      "en": {
        "title": "Example: screenshot schedule from chat (stable URI)",
        "cta_label": "Try a question in chat",
        "cta_hint": "Line 3 of the Taskinity Chat batch demo plans this workflow.",
        "body": "A typical site monitoring pilot — NL chat, stable workflow, optional cron:\n\n```\n1. NL chat (batch)     →  workflow://graph/website-screenshot-schedule/dry-run\n2. Dry-run / approve   →  mock browser or Playwright → ~/images/\n3. Host cron (opt.)    →  cron://www/monitor/landing + install-cron.sh\n4. Taskinity           →  health every 5 min + logs + chat on failure\n```\n\n- A prompt like “take screenshots of these sites…” does **not** create a random `domain://` slug — same workflow ID every time.\n- `bash examples/35_website_screenshot_schedule/run.sh` — PASS in CI.\n- After edits: `make www-docs` and restart the WWW container (Docker).\n"
      },
      "de": {
        "title": "Beispiel: Screenshot-Zeitplan aus Chat (stabile URI)",
        "cta_label": "Frage im Chat testen",
        "cta_hint": "Zeile 3 der Taskinity-Chat-Batch-Demo plant diesen Workflow.",
        "body": "Typischer Site-Monitoring-Pilot — NL-Chat, stabiler Workflow, optional Cron:\n\n```\n1. NL-Chat (Batch)     →  workflow://graph/website-screenshot-schedule/dry-run\n2. Dry-run / Approve   →  Mock-Browser oder Playwright → ~/images/\n3. Host-Cron (opt.)    →  cron://www/monitor/landing + install-cron.sh\n4. Taskinity           →  Health alle 5 Min + Logs + Chat bei Ausfall\n```\n\n- Prompts wie „Screenshots dieser Seiten…” erzeugen **keine** zufällige `domain://`-URI — immer dieselbe Workflow-ID.\n- `bash examples/35_website_screenshot_schedule/run.sh` — PASS in CI.\n- Nach Änderungen: `make www-docs` und WWW-Container neu starten (Docker)."
      }
    }
  }
};
