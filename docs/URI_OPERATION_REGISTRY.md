# URI Operation Registry

The registry maps URI schemes and operation names to executable handlers and CQRS semantics.

A scheme registry answers: "Is `browser://...` valid?"

An operation registry answers: "What can I do with `browser://...`, what schema validates it, and what handler runs it?"

Example:

```yaml
browser:
  operations:
    open:
      kind: command
      handler: python://uri2ops.operator.adapters.browser_mock:open_page
      input_schema: operator.browser.v1.BrowserPageOpenCommand
      side_effects: true
      requires_policy: true
```

Rules:

- `query` operations should not mutate external state.
- `command` operations may mutate state and should require policy approval unless explicitly allowed.
- Large outputs are artifacts, not event payloads.
- Secrets are never written to events.
