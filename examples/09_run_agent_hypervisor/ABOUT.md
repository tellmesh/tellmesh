---
landing:
  cards:
    - id: run-agent-connector
      layout: connector
      order: 35
      logo: RA
      docs: docs/examples.html#ex-09_run_agent_hypervisor
      i18n:
        pl:
          tag: Hypervisor
          title: Uruchamianie agenta przez hypervisor
          lead: urish / hypervisor zarządza lifecycle agenta (run, detach, health, repair) — jeden interfejs dla wszystkich.
        en:
          tag: Hypervisor
          title: Running agent via hypervisor
          lead: urish / hypervisor manages agent lifecycle (run, detach, health, repair) — single interface for all.
        de:
          tag: Hypervisor
          title: Agent über Hypervisor starten
          lead: urish / Hypervisor verwaltet den Agent-Lebenszyklus (run, detach, health, repair).
      snippet: |
        NL: "uruchom agenta invoices-agent.local z hypervisora"
        URI: hypervisor://local/invoices-agent.local/run
        Run: urish agent run invoices-agent.local --detach

    - id: run-agent-card
      layout: card
      order: 45
      docs: docs/examples.html#ex-09_run_agent_hypervisor
      i18n:
        pl:
          tag: Lifecycle
          title: run-agent · health · repair
        en:
          tag: Lifecycle
          title: run-agent · health · repair
        de:
          tag: Lebenszyklus
          title: run-agent · health · repair
      snippet: |
        urish agent run my-agent.local --detach
        urish agent health my-agent.local
        urish repair diagnose my-agent.local
---
<ul>
<li>Centralne zarządzanie agentami (deployment registry, runtime state).</li>
<li>Detached + watch + repair loops — agenci działają autonomicznie.</li>
<li>file:// i log:// dla inspekcji źródeł i logów procesu.</li>
</ul>
