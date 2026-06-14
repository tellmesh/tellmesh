# uri2verify

Shared verification layer for the URI stack:

```txt
data_quality   — confidence, validators, relevance gates
replay         — workflow event log analysis + regression test generation
capability_plan — contract registry capability test plans
```

Used by `touri`, `uri3` CLI, and `hypervisor`.

## Examples

```bash
uri3 replay-failure output/events/workflows/check-agent-health.jsonl
hypervisor replay-failure check-agent-health --create-test tests/replay/test_check_agent_health.py
```

See [`docs/PACKAGE_BOUNDARIES.md`](../../docs/PACKAGE_BOUNDARIES.md).
