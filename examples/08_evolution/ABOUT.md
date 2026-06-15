---
landing:
  cards:
    - id: evolution-connector
      layout: connector
      order: 32
      logo: EV
      docs: docs/examples.html#ex-08_evolution
      i18n:
        pl:
          tag: Ewolucja
          title: Propozycje ewolucji agentów z ticketów/incydentów
          lead: Z ticketu lub incidentu powstaje proposal ewolucji → verify → apply.
        en:
          tag: Evolution
          title: Evolution proposals from tickets/incidents
          lead: From ticket or incident → evolution proposal → verify → apply.
        de:
          tag: Evolution
          title: Evolutionsvorschläge aus Tickets/Incidents
          lead: Aus Ticket oder Incident → Evolutionsvorschlag → verify → apply.
      snippet: |
        NL: "stwórz propozycję ewolucji na podstawie incydentu"
        Dir: examples/08_evolution/proposals/

    - id: evolution-card
      layout: card
      order: 42
      docs: docs/examples.html#ex-08_evolution
      i18n:
        pl:
          tag: Propozycje
          title: proposals · verify · apply
        en:
          tag: Proposals
          title: proposals · verify · apply
        de:
          tag: Vorschläge
          title: proposals · verify · apply
      snippet: |
        urish proposal verify examples/08_evolution/proposals/add_*.yaml
        urish proposal apply ... --approve
---
<ul>
<li>Automatyczna ewolucja systemu na podstawie rzeczywistych awarii/ticketów.</li>
<li>Propozycje w evolution/proposals/ — weryfikowalne i stosowalne przez urish.</li>
<li>Pełny cykl: detect → propose → verify → apply (z file:// dla źródeł).</li>
</ul>
