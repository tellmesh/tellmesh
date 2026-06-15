---
landing:
  cards:
    - id: pcwin-operator-connector
      layout: connector
      order: 58
      logo: PC
      docs: docs/examples.html#ex-13_pcwin_operator
      i18n:
        pl:
          tag: PC Win
          title: Operator Windows (Subiekt, UI)
          lead: pcwin://window/Subiekt/focus + wpisywanie — automatyzacja legacy Windows apps.
        en:
          tag: PC Win
          title: Windows operator (Subiekt, UI)
          lead: pcwin://window/Subiekt/focus + typing — legacy Windows app automation.
        de:
          tag: PC Win
          title: Windows-Operator (Subiekt, UI)
          lead: pcwin://window/Subiekt/focus + Eingabe — Legacy-Windows-App-Automatisierung.
      snippet: |
        NL: "otwórz Subiekt i wystaw fakturę"
        Task: examples/13_pcwin_operator/task.pcwin.yaml

    - id: pcwin-operator-card
      layout: card
      order: 68
      docs: docs/examples.html#ex-13_pcwin_operator
      i18n:
        pl:
          tag: Legacy UI
          title: pcwin + windows UIA
        en:
          tag: Legacy UI
          title: pcwin + windows UIA
        de:
          tag: Legacy UI
          title: pcwin + windows UIA
      snippet: |
        urish run task.pcwin.yaml --approve
---
<ul>
<li>Obsługa aplikacji desktopowych bez API (Subiekt, inne ERP).</li>
<li>task.pcwin.yaml + operator — spójne z Android/browser.</li>
<li>Logi i artefakty z file:// dla audytu.</li>
</ul>
