# Example 08 — evolution proposals

Przykładowe propozycje autoewolucji agentów walidowane przez `hypervisor.evolution`.

Katalog:

```txt
examples/08_evolution/proposals/*.yaml
```

Walidacja:

```bash
python -m hypervisor.evolution.cli examples/08_evolution/proposals/*.yaml
```

Pliki:

- [`proposals/add_orders_agent.yaml`](./proposals/add_orders_agent.yaml) — dodanie agenta zamówień
- [`proposals/add_invoices_agent.yaml`](./proposals/add_invoices_agent.yaml) — dodanie agenta faktur z promptem i approval gate

Powiązane przykłady:

- [`../06_orders_agent/`](../06_orders_agent/) — przykładowy kontrakt orders
- [`../07_invoices_agent/`](../07_invoices_agent/) — prompt invoices
