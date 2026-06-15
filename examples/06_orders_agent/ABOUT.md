---
landing:
  cards:
    - id: orders-agent-connector
      layout: connector
      order: 25
      logo: OR
      docs: docs/examples.html#ex-06_orders_agent
      i18n:
        pl:
          tag: Orders
          title: Tworzenie agenta zamówień z YAML
          lead: create_orders_agent.yaml → generator → wygenerowany agent + kontrakt + deployment.
        en:
          tag: Orders
          title: Create orders agent from YAML
          lead: create_orders_agent.yaml → generator → generated agent + contract + deployment.
        de:
          tag: Bestellungen
          title: Erstellung eines Bestell-Agenten aus YAML
          lead: create_orders_agent.yaml → Generator → generierter Agent + Vertrag + Deployment.
      snippet: |
        NL: "utwórz agenta do zamówień z pliku create_orders_agent.yaml"
        Command: generator or urish ecosystem plan examples/06_orders_agent

    - id: orders-agent-card
      layout: card
      order: 35
      docs: docs/examples.html#ex-06_orders_agent
      i18n:
        pl:
          tag: YAML → agent
          title: create_*.yaml · generator · apply
        en:
          tag: YAML → agent
          title: create_*.yaml · generator · apply
        de:
          tag: YAML → Agent
          title: create_*.yaml · Generator · Apply
      snippet: |
        urish ecosystem plan examples/06_orders_agent --profile agent
        urish ecosystem apply ...
---
<ul>
<li>Prosty kontrakt YAML → pełny wygenerowany agent w agents/generated/.</li>
<li>Plik .generated.yaml z file:// do markpact_readme (README.md z blokami).</li>
<li>Gotowy do deploy przez urish agent run lub ecosystem.</li>
</ul>
