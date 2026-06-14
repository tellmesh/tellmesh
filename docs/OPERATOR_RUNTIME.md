# Operator Runtime

`uri2ops` executes URI task graphs through adapters.

Flow:

```txt
URI task graph
  -> validate
  -> dependency sort
  -> policy check
  -> dispatch operation
  -> adapter execution
  -> event JSONL + artifact URI
```

The first implementation uses mock adapters. Real adapters should be added as optional extras.

Recommended order:

1. Mock browser adapter.
2. Playwright browser adapter.
3. Android ADB adapter.
4. Windows UI Automation adapter.
5. Remote `uri2ops serve` daemon.
