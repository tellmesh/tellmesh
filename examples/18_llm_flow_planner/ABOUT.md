---
landing:
  cards:
    - id: llm-flow-connector
      layout: connector
      order: 100
      logo: LF
      docs: docs/examples.html#ex-18_llm_flow_planner
      i18n:
        pl:
          tag: LLM Flow
          title: LLM do generowania compact flow
          lead: Prompt + LLM → compact .uri.flow.yaml (z branchami) — potem expand do graph.
        en:
          tag: LLM Flow
          title: LLM for compact flow generation
          lead: Prompt + LLM → compact .uri.flow.yaml (with branches) — then expand to graph.
        de:
          tag: LLM Flow
          title: LLM zur Generierung kompakter Flows
          lead: Prompt + LLM → kompakte .uri.flow.yaml (mit Branches) — dann Expand zum Graph.
      snippet: |
        NL: "użyj LLM do zrobienia flow z promptu"
        Prompt: examples/18_llm_flow_planner/prompt.txt
        Run: bash .../run.sh (LLM key or rule-based)

    - id: llm-flow-card
      layout: card
      order: 110
      docs: docs/examples.html#ex-18_llm_flow_planner
      i18n:
        pl:
          tag: LLM + flow
          title: llm + uri2flow
        en:
          tag: LLM + flow
          title: llm + uri2flow
        de:
          tag: LLM + flow
          title: llm + uri2flow
      snippet: |
        urish nl "..." --llm --out flow.yaml
        urish uri2flow expand flow.yaml
---
<ul>
<li>LLM pomaga pisać czytelne compact flows.</li>
<li>Połączone z rule-based fallback.</li>
<li>Wynik zawsze expandowalny i wykonywalny (file:// + validate).</li>
</ul>
