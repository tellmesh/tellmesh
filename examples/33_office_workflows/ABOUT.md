---
landing:
  cards:
    - id: portal-connector
      layout: connector
      order: 60
      logo: WWW
      docs: docs/examples.html#ex-33_office_workflows
      i18n:
        pl:
          tag: Strony i portale
          title: Logowanie, pobieranie danych, formularze
          lead: Playwright lub browser adapter wykonuje czynności w portalu, robi screenshot i zatrzymuje się przed wysyłką danych.
        en:
          tag: Websites & portals
          title: Login, data fetch, forms
          lead: Playwright or browser adapter acts in the portal, captures a screenshot and stops before submitting data.
        de:
          tag: Webseiten & Portale
          title: Login, Datenabruf, Formulare
          lead: Playwright oder Browser-Adapter arbeitet im Portal, Screenshot und Stopp vor dem Absenden.
      snippet: |
        NL: "pobierz raport CSV z portalu dostawcy"
        URI: workflow://office/supplier-report/monthly
        Proof: artifact://workflow/.../screenshot.png

    - id: portal-card
      layout: card
      order: 105
      docs: docs/examples.html#ex-33_office_workflows
      i18n:
        pl:
          tag: Portale · WWW
          title: Portal dostawcy · raport CSV
        en:
          tag: Portals · WWW
          title: Supplier portal · CSV report
        de:
          tag: Portale · WWW
          title: Lieferantenportal · CSV-Bericht
      snippet: |
        bash examples/33_office_workflows/run.sh
---

<p>Zobacz też <a href="docs/examples.html#ex-33_office_workflows">office workflows</a> i kartę biurową „Website”.</p>
