---
landing:
  cards:
    - id: workflow-exec-mock-connector
      layout: connector
      order: 65
      logo: WEM
      docs: docs/examples.html#ex-14_workflow_executor_mock
      i18n:
        pl:
          tag: Workflow
          title: Mock executor dla task_graph / workflow
          lead: task_graph.yaml → dry-run / execute z mock adapterami — testy bez realnych side-effects.
        en:
          tag: Workflow
          title: Mock executor for task_graph / workflow
          lead: task_graph.yaml → dry-run / execute with mock adapters — tests without real side-effects.
        de:
          tag: Workflow
          title: Mock-Executor für task_graph / workflow
          lead: task_graph.yaml → Dry-run / Execute mit Mock-Adaptern.
      snippet: |
        NL: "wykonaj task graph z mockiem"
        Graph: examples/14_workflow_executor_mock/task_graph.yaml
        Run: bash .../run.sh

    - id: workflow-exec-mock-card
      layout: card
      order: 75
      docs: docs/examples.html#ex-14_workflow_executor_mock
      i18n:
        pl:
          tag: Testy
          title: executor mock + dry-run
        en:
          tag: Tests
          title: executor mock + dry-run
        de:
          tag: Tests
          title: executor mock + dry-run
      snippet: |
        urish run task_graph.yaml --dry-run
        urish run ... --approve --adapter mock
---
<ul>
<li>Bezpieczne testowanie grafów przed realnym wykonaniem.</li>
<li>Porównanie z real adapters (browser, android).</li>
<li>Eventy i artefakty w output/ — file:// do inspekcji.</li>
</ul>
