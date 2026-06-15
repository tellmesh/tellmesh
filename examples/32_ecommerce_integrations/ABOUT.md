---
landing:
  cards:
    - id: woocommerce-connector
      layout: connector
      order: 20
      logo: WC
      docs: docs/examples.html#ex-32_ecommerce_integrations
      i18n:
        pl:
          tag: WooCommerce
          title: Zamówienie do faktury i magazynu
          lead: Webhook sklepu uruchamia workflow — pobierz zamówienie, sprawdź płatność, wystaw fakturę i zsynchronizuj stan.
        en:
          tag: WooCommerce
          title: Order to invoice and inventory
          lead: Store webhook runs a workflow — fetch order, verify payment, issue invoice and sync stock.
        de:
          tag: WooCommerce
          title: Bestellung zu Rechnung und Lager
          lead: Shop-Webhook startet Workflow — Bestellung holen, Zahlung prüfen, Rechnung und Bestand syncen.
      snippet: |
        NL: "pilnuj zamówień WooCommerce i fakturuj po płatności"
        URI: workflow://order/woocommerce-to-erp
        Health: health://agent/invoices-agent.local

    - id: baselinker-connector
      layout: connector
      order: 30
      logo: BL
      docs: docs/examples.html#ex-32_ecommerce_integrations
      i18n:
        pl:
          tag: BaseLinker
          title: Marketplace hub bez ślepych cronów
          lead: Cron lub n8n woła API BaseLinker, a Taskinity porównuje zamówienia, stany i błędy synchronizacji z ERP.
        en:
          tag: BaseLinker
          title: Marketplace hub without blind crons
          lead: Cron or n8n calls BaseLinker API; Taskinity compares orders, stock and sync errors with ERP.
        de:
          tag: BaseLinker
          title: Marketplace-Hub ohne blinde Cronjobs
          lead: Cron oder n8n ruft BaseLinker-API; Taskinity vergleicht Bestellungen, Bestand und Sync-Fehler mit ERP.
      snippet: |
        NL: "sprawdź rozjazd stanów BaseLinker i WooCommerce"
        URI: workflow://sync/baselinker-inventory
        Repair: repair://agent/baselinker-sync.local/diagnose

    - id: allegro-connector
      layout: connector
      order: 40
      logo: AL
      docs: docs/examples.html#ex-32_ecommerce_integrations
      i18n:
        pl:
          tag: Allegro.pl
          title: OAuth, zamówienia, zwroty
          lead: Agent pilnuje tokenu OAuth, pobiera checkout forms, wykrywa 429/503 i pokazuje w chacie, które zamówienie utknęło.
        en:
          tag: Allegro.pl
          title: OAuth, orders, returns
          lead: Agent manages OAuth token, fetches checkout forms, detects 429/503 and shows stuck orders in chat.
        de:
          tag: Allegro.pl
          title: OAuth, Bestellungen, Retouren
          lead: Agent verwaltet OAuth-Token, lädt Checkout Forms, erkennt 429/503 und zeigt hängende Bestellungen im Chat.
      snippet: |
        NL: "zdiagnozuj synchronizację Allegro z ERP"
        URI: workflow://allegro/orders-to-erp
        Logs: log://agent/allegro-sync.local?level=error

    - id: woocommerce-card
      layout: card
      order: 120
      docs: docs/examples.html#ex-32_ecommerce_integrations
      i18n:
        pl:
          tag: WooCommerce
          title: Sklep · zamówienia · stany
        en:
          tag: WooCommerce
          title: Store · orders · stock
        de:
          tag: WooCommerce
          title: Shop · Bestellungen · Bestand
      snippet: |
        # WooCommerce REST (Consumer key)
        GET /wp-json/wc/v3/orders?status=processing
        → agent invoices-agent.local → ERP / Baselinker
      body: |
        <ul>
        <li>Webhook <code>order.created</code> / <code>order.updated</code> → agent faktur lub magazynu.</li>
        <li>Health na endpoint Woo REST — widać od razu, czy synchronizacja stoi.</li>
        <li>Chat: „dlaczego zamówienie #4521 nie poszło do Baselinkera?”</li>
        </ul>

    - id: baselinker-card
      layout: card
      order: 130
      docs: docs/examples.html#ex-32_ecommerce_integrations
      i18n:
        pl:
          tag: Baselinker
          title: Magazyn · marketplace hub
        en:
          tag: BaseLinker
          title: Warehouse · marketplace hub
        de:
          tag: BaseLinker
          title: Lager · Marketplace-Hub
      snippet: |
        uri run workflow://sync/baselinker-inventory/dry-run
        uri run workflow://sync/baselinker-inventory --approve
      body: |
        <ul>
        <li>API Baselinker (<code>getOrders</code>, <code>updateInventory</code>) jako krok workflow URI.</li>
        <li>Cron co N minut + porównanie liczby zamówień vs WooCommerce / Allegro.</li>
        </ul>

    - id: allegro-card
      layout: card
      order: 140
      docs: docs/examples.html#ex-32_ecommerce_integrations
      i18n:
        pl:
          tag: Allegro.pl
          title: Aukcje · zamówienia · OAuth
        en:
          tag: Allegro.pl
          title: Auctions · orders · OAuth
        de:
          tag: Allegro.pl
          title: Auktionen · Bestellungen · OAuth
      snippet: |
        GET https://api.allegro.pl/order/checkout-forms
        → workflow://allegro/orders-to-erp
      body: |
        <ul>
        <li>Agent z tokenem OAuth Allegro — pobieranie zamówień, status wysyłki, zwroty.</li>
        <li>Przy 429/503: supervisor retry z backoff, incident zamiast cichego failu.</li>
        </ul>

    - id: ecommerce-spotlight
      layout: spotlight
      order: 200
      cta:
        href: chat.html
      i18n:
        en:
          title: "Example: WooCommerce → BaseLinker → ERP (one view)"
          cta_label: Try a question in chat
          cta_hint: The 3-process pilot covers exactly this layout.
          body: |
            Typical e-commerce pilot — three systems, one chat on failure:

            ```
            1. WooCommerce webhook  →  workflow://order/new
            2. BaseLinker sync      →  shell://scripts/sync-baselinker.sh
            3. ERP invoice          →  http://erp.local/api/invoices  (agent invoices-agent.local)
            4. Taskinity            →  health every 5 min + webhook alert + NL chat

            # when something breaks:
            "Diagnose Allegro sync and show latest ERP errors"
            → repair://agent/invoices-agent.local/diagnose
            ```

            - Webhook `order.created` / `order.updated` → invoice or warehouse agent.
            - Health on Woo REST endpoint — see immediately if sync is stuck.
            - Chat: “why did order #4521 not reach BaseLinker?”

            - BaseLinker API (`getOrders`, `updateInventory`) as a workflow URI step.
            - Cron every N minutes + order count vs WooCommerce / Allegro.

            - Agent with Allegro OAuth token — orders, shipping status, returns.
            - On 429/503: supervisor retry with backoff, incident instead of silent fail.
        pl:
          title: "Przykład: WooCommerce → Baselinker → ERP (jeden widok)"
          cta_label: Wypróbuj pytanie w chacie
          cta_hint: Pilot 3 procesów obejmuje właśnie taki układ.
          body: |
            Typowy pilot e-commerce — trzy systemy, jeden chat przy awarii:

            ```
            1. WooCommerce webhook  →  workflow://order/new
            2. Baselinker sync      →  shell://scripts/sync-baselinker.sh
            3. ERP faktura          →  http://erp.local/api/invoices  (agent invoices-agent.local)
            4. Taskinity            →  health co 5 min + webhook alert + chat NL

            # gdy coś padnie:
            "Zdiagnozuj synchronizację Allegro i pokaż ostatnie błędy ERP"
            → repair://agent/invoices-agent.local/diagnose
            ```

            - Webhook `order.created` / `order.updated` → agent faktur lub magazynu.
            - Health na endpoint Woo REST — widać od razu, czy synchronizacja stoi.
            - Chat: „dlaczego zamówienie #4521 nie poszło do Baselinkera?”

            - API Baselinker (`getOrders`, `updateInventory`) jako krok workflow URI.
            - Cron co N minut + porównanie liczby zamówień vs WooCommerce / Allegro.

            - Agent z tokenem OAuth Allegro — pobieranie zamówień, status wysyłki, zwroty.
            - Przy 429/503: supervisor retry z backoff, incident zamiast cichego failu.
        de:
          title: "Beispiel: WooCommerce → BaseLinker → ERP (eine Ansicht)"
          cta_label: Frage im Chat testen
          cta_hint: Der 3-Prozess-Pilot deckt genau dieses Layout ab.
          body: |
            Typischer E-Commerce-Pilot — drei Systeme, ein Chat bei Ausfall:

            ```
            1. WooCommerce Webhook  →  workflow://order/new
            2. BaseLinker Sync      →  shell://scripts/sync-baselinker.sh
            3. ERP Rechnung         →  http://erp.local/api/invoices  (Agent invoices-agent.local)
            4. Taskinity            →  Health alle 5 Min + Webhook + NL-Chat

            # bei Ausfall:
            "Allegro-Sync diagnostizieren und letzte ERP-Fehler zeigen"
            → repair://agent/invoices-agent.local/diagnose
            ```

            - Webhook `order.created` / `order.updated` → Rechnungs- oder Lager-Agent.
            - Health auf Woo-REST — sofort sichtbar, ob Sync hängt.
            - Chat: „warum ging Bestellung #4521 nicht zu BaseLinker?”

            - BaseLinker API (`getOrders`, `updateInventory`) als Workflow-URI-Schritt.
            - Cron alle N Minuten + Bestellvergleich WooCommerce / Allegro.

            - Agent mit Allegro-OAuth — Bestellungen, Versandstatus, Retouren.
            - Bei 429/503: Supervisor-Retry mit Backoff, Incident statt stillem Fail.
---
