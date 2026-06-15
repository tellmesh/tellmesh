---
landing:
  cards:
    - id: erp-connector
      layout: connector
      order: 50
      logo: ERP
      docs: docs/examples.html#ex-31_office_day
      i18n:
        pl:
          tag: ERP · CRM
          title: Comarch, Subiekt, HubSpot, Salesforce
          lead: REST, SOAP, CSV, SQL albo okna Windows. System rozdziela automatyczne kroki od tych, które wymagają akceptacji człowieka.
        en:
          tag: ERP · CRM
          title: Comarch, Subiekt, HubSpot, Salesforce
          lead: REST, SOAP, CSV, SQL or Windows UI. Automatic steps vs human approval are separated.
        de:
          tag: ERP · CRM
          title: Comarch, Subiekt, HubSpot, Salesforce
          lead: REST, SOAP, CSV, SQL oder Windows-UI — automatische vs manuelle Schritte getrennt.
      snippet: |
        NL: "wystaw faktury w ERP i pokaż podgląd"
        URI: workflow://invoices/batch/dry-run
        UI: pcwin://window/Subiekt/focus

    - id: erp-card
      layout: card
      order: 100
      docs: docs/examples.html#ex-31_office_day
      i18n:
        pl:
          tag: ERP · CRM
          title: Comarch · Subiekt · Salesforce · HubSpot
        en:
          tag: ERP · CRM
          title: Comarch · Subiekt · Salesforce · HubSpot
        de:
          tag: ERP · CRM
          title: Comarch · Subiekt · Salesforce · HubSpot
      snippet: |
        urish ask "zdiagnozuj agenta invoices-agent.local"
        # → repair://agent/invoices-agent.local/diagnose
---

<ul>
<li>Cron lub n8n woła REST ERP → agent zapisuje wynik i logi błędów 401/500.</li>
<li>Przy awarii: incident z kontekstem (endpoint, payload, ostatni sukces).</li>
<li>Ticket do developera z gotowym planem naprawy — bez ręcznego kopiowania logów.</li>
</ul>
