# Example 34 — `cron://` URI schedules

Taskinity exposes recurring host jobs as **`cron://`** capabilities via **touri**
(manifest YAML → `uri explain` / `uri call` / chat).

> **Note:** `cron://` is not a built-in uri3 resolver scheme. It is registered in
> [`examples/20_touri_capabilities/`](../20_touri_capabilities/) and executed through
> touri → `shell` backend (same path as `workflow://` in chat/dashboard).

## URI

| URI | Schedule | Command |
|-----|----------|---------|
| `cron://www/monitor/landing` | `*/5 * * * *` | `python scripts/www/monitor_landing.py --url http://localhost:8788/www/` |

Manifest: [`www_landing_monitor_cron.uri.capability.yaml`](../20_touri_capabilities/www_landing_monitor_cron.uri.capability.yaml)

## Quick start

WWW server running (`make start` or `urish www serve`):

```bash
bash examples/34_cron_uri/run.sh
```

Manual steps:

```bash
# Explain (resolution via touri registry)
uri explain cron://www/monitor/landing

# Dry-run (plan only — no shell execution)
uri call cron://www/monitor/landing --dry-run

# Run once (monitor script; needs :8788 up)
uri call cron://www/monitor/landing --approve

# Install host crontab entry (every 5 min)
bash scripts/www/install-cron.sh --install
bash scripts/www/install-cron.sh --status
```

## Chat / dashboard

```text
cron://www/monitor/landing
```

Use **dry-run** first. For a one-shot run use **Run real** (approve).

## Related

- [`16_www_landing_monitor`](../16_www_landing_monitor/) — uri3 workflow graph monitor
- [`scripts/www/monitor_landing.py`](../../scripts/www/monitor_landing.py)
- [`scripts/www/install-cron.sh`](../../scripts/www/install-cron.sh)
- Docs: `www/docs/examples.html#ex-34_cron_uri`
