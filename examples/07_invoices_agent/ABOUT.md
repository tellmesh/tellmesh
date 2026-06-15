---
landing:
  cards:
    - id: invoices-agent-connector
      layout: connector
      order: 28
      logo: IN
      docs: docs/examples.html#ex-07_invoices_agent
      i18n:
        pl:
          tag: Invoices
          title: Agent faktur z promptu NL
          lead: Prompt w pliku → nl2a / generator → agent + capabilities do batch faktur.
        en:
          tag: Invoices
          title: Invoices agent from NL prompt
          lead: Prompt in file → nl2a / generator → agent + capabilities for batch invoices.
        de:
          tag: Rechnungen
          title: Rechnungs-Agent aus NL-Prompt
          lead: Prompt in Datei → nl2a / Generator → Agent + Capabilities für Batch-Rechnungen.
      snippet: |
        NL: "utwórz agenta do faktur z create_invoices_agent_prompt.txt"
        Prompt: examples/07_invoices_agent/create_invoices_agent_prompt.txt

    - id: invoices-agent-card
      layout: card
      order: 38
      docs: docs/examples.html#ex-07_invoices_agent
      i18n:
        pl:
          tag: Prompt → agent
          title: Prompt txt · nl2a · generated
        en:
          tag: Prompt → agent
          title: Prompt txt · nl2a · generated
        de:
          tag: Prompt → Agent
          title: Prompt txt · nl2a · generiert
      snippet: |
        nl2a -p "$(cat examples/07_invoices_agent/create_invoices_agent_prompt.txt)"
---
<ul>
<li>Prompt NL w pliku txt → wygenerowany agent invoices w agents/generated/.</li>
<li>Integracja z batch workflows (patrz 33_office_workflows).</li>
<li>Markpact w README + file:// w markerze po generacji.</li>
</ul>
