# Scenario registries

NL routing registries for `urish ask` live here and under `domains/*/`.

| Location | Domain |
|----------|--------|
| [`domains/office/scenario_registry.yaml`](../../domains/office/scenario_registry.yaml) | Office automation (canonical) |
| [`domains/office/README.md`](../../domains/office/README.md) | `markpact:scenario` export blocks |

Override loader path:

```bash
URISH_SCENARIO_REGISTRY=domains/office urish ask "..."
```
