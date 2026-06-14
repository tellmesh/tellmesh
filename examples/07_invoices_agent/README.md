# Example 07 — prompt agenta faktur

Przykładowy prompt naturalny do wygenerowania agenta faktur.

Plik:

```txt
examples/07_invoices_agent/create_invoices_agent_prompt.txt
```

Przykładowe użycie:

```bash
python -m meta_agent.cli plan "$(cat examples/07_invoices_agent/create_invoices_agent_prompt.txt)"
python -m meta_agent.cli pipeline "$(cat examples/07_invoices_agent/create_invoices_agent_prompt.txt)"
```

Powiązany evolution proposal: [`../08_evolution/proposals/add_invoices_agent.yaml`](../08_evolution/proposals/add_invoices_agent.yaml).
