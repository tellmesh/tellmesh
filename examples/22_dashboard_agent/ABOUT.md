---
landing:
  cards:
    - id: dashboard-agent-connector
      layout: connector
      order: 140
      logo: DA
      docs: docs/examples.html#ex-22_dashboard_agent
      i18n:
        pl:
          tag: Dashboard
          title: Agent dashboard (health, incidents, repair)
          lead: Dashboard agent z capabilities do podglądu health, incydentów i repair — UI + API.
        en:
          tag: Dashboard
          title: Dashboard agent (health, incidents, repair)
          lead: Dashboard agent with capabilities for health view, incidents and repair — UI + API.
        de:
          tag: Dashboard
          title: Dashboard-Agent (Health, Incidents, Repair)
          lead: Dashboard-Agent mit Capabilities für Health-View, Incidents und Repair.
      snippet: |
        NL: "pokaż dashboard agenta i incydenty"
        Caps: dashboard_open.uri.flow.yaml + incident_explain...
        Run: urish dashboard create ...

    - id: dashboard-agent-card
      layout: card
      order: 150
      docs: docs/examples.html#ex-22_dashboard_agent
      i18n:
        pl:
          tag: UI Agent
          title: dashboard + repair + process view
        en:
          tag: UI Agent
          title: dashboard + repair + process view
        de:
          tag: UI Agent
          title: dashboard + repair + process view
      snippet: |
        urish dashboard open
        urish call process_view...
---
<ul>
<li>Agent jako web UI dla systemu (health, repair, incidents).</li>
<li>Capabilities do flow i direct call.</li>
<li>Integracja z www/ i chat.</li>
</ul>
