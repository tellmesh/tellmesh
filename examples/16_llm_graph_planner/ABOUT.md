---
landing:
  cards:
    - id: llm-graph-connector
      layout: connector
      order: 82
      logo: LG
      docs: docs/examples.html#ex-16_llm_graph_planner
      i18n:
        pl:
          tag: LLM Graph
          title: LLM do planowania grafu (task/workflow)
          lead: Prompt + LLM → task_graph lub workflow_graph (zależnie od promptu).
        en:
          tag: LLM Graph
          title: LLM for graph planning (task/workflow)
          lead: Prompt + LLM → task_graph or workflow_graph (depends on prompt).
        de:
          tag: LLM Graph
          title: LLM für Graph-Planung (Task/Workflow)
          lead: Prompt + LLM → task_graph oder workflow_graph.
      snippet: |
        NL: "użyj LLM do zaplanowania grafu dla promptu"
        Prompt: examples/16_llm_graph_planner/prompt.txt
        Run: bash .../run.sh (with LLM key or --no-llm)

    - id: llm-graph-card
      layout: card
      order: 92
      docs: docs/examples.html#ex-16_llm_graph_planner
      i18n:
        pl:
          tag: LLM
          title: llm_graph_planner + graph
        en:
          tag: LLM
          title: llm_graph_planner + graph
        de:
          tag: LLM
          title: llm_graph_planner + graph
      snippet: |
        urish nl "..." --llm
---
<ul>
<li>LLM wspiera planowanie złożonych grafów.</li>
<li>Porównanie z rule-based (17_flow_vs_graph).</li>
<li>Wynik: task_graph.yaml lub expanded graph.</li>
</ul>
