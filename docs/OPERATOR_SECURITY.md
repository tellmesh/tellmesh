# Operator Security

Operator execution can control browser, input, OS windows, or devices. Treat it as high-risk automation.

Rules:

- Commands with side effects require approval by default.
- Do not pass secrets in URI query strings.
- Do not log typed secret values.
- Do not store screenshots or DOM as event payloads.
- Store artifacts separately and reference them with `artifact://...`.
- Event logs store metadata, hashes, and artifact URIs only.

Suggested risk levels:

- `observe`: screenshot, DOM read, UI tree dump.
- `navigate`: open URL or app.
- `input`: typing/clicking.
- `submit`: confirming or sending.
- `system`: shell/installer/system changes.
