# Example 16 — LLM Graph Planner (v0.6.3)

Rule-based fallback (no API key):

```bash
nl2uri graph -p "$(cat prompt.txt)" --validate --dry-run
```

LLM planner with operation registry injection:

```bash
export OPENROUTER_API_KEY=...
nl2uri graph -p "$(cat prompt.txt)" --llm --validate --dry-run
```

Execute validated workflow with mock browser:

```bash
nl2uri graph -p "$(cat prompt.txt)" --validate > /tmp/workflow.yaml
uri3 run-workflow /tmp/workflow.yaml --dry-run
uri3 run-workflow /tmp/workflow.yaml --approve --browser mock
```

If the LLM returns invalid schemes or operations, nl2uri repairs what it can and falls back to the rule-based planner when validation still fails.
