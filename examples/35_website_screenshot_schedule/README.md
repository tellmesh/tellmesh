# Example 35 — Website screenshot schedule (chat NL)

Chat prompts like “rob rzuty ekranów stron softreck.com prototypowanie.pl co 5 minut
do folderu ~/images/” plan a **stable** workflow URI:

| URI | Mode |
|-----|------|
| `workflow://graph/website-screenshot-schedule/dry-run` | Plan only (mock browser) |
| `workflow://graph/website-screenshot-schedule` | Execute with approval |

Manifests: [`website_screenshot_schedule_dry_run.uri.capability.yaml`](../20_touri_capabilities/website_screenshot_schedule_dry_run.uri.capability.yaml)

Source files (task graph, this README as provenance) are now addressable via native `file://` URIs. The system (path resolution in uri2run, graph loading in uri3, markpact loaders in uri2pact) supports `file://` alongside `markpact://file://...` for generated agent/workflow sources and logs.

Example:
```
file://$(pwd)/examples/35_website_screenshot_schedule/task_graph.yaml
file://$(pwd)/examples/35_website_screenshot_schedule/README.md
```
(See `packages/uri2pact/uri2pact/core.py`, `uri2run/transports/paths.py`, `uri3/graph/graph_validator.py` for the `file://` support rollout.)

## Quick start

```bash
bash examples/35_website_screenshot_schedule/run.sh
```

Manual:

```bash
uri explain workflow://graph/website-screenshot-schedule/dry-run
uri run workflow://graph/website-screenshot-schedule/dry-run
uri run workflow://graph/website-screenshot-schedule --approve --adapter mock
```

Real PNG captures (optional):

```bash
pip install -e '.[browser]'
playwright install chromium
uri run workflow://graph/website-screenshot-schedule --approve --adapter playwright
```

Recurring host schedule is **not** auto-installed by chat — use `scripts/www/install-cron.sh`
or wire a custom cron entry that calls the workflow URI.

**Watching logs live with `log://` in watch mode (via urish / uri):**

Run the workflow in one terminal (use `--adapter mock` to avoid sync/async playwright issues with real browser inside the flow executor asyncio context):

```bash
urish run workflow://graph/website-screenshot-schedule --approve --adapter mock
```

In another terminal, watch logs using log:// URI:

```bash
# Watch hypervisor logs filtered for this schedule (live, Ctrl-C to stop)
urish watch 'log://hypervisor?grep=website-screenshot-schedule|open|screenshot|browser' --interval 1

# Or one-shot recent entries
urish logs 'log://hypervisor?grep=website-screenshot-schedule&limit=50'

# Watch a specific file log (e.g. process log)
urish watch 'log://file/output/logs/hypervisor.log?grep=website' --interval 2

# Direct "uri" (via fallback)
uri watch 'log://hypervisor?grep=website-screenshot-schedule' --interval 1
```

The `urish watch` / `uri watch` for `log://` polls and emits RuntimeEvent snapshots with the log summary.

See `packages/urish/urish/commands/observe_commands.py` and `backends/watch.py` (and `read_log_uri`).

**file:// URI support** (rolled out for markpact sources, graphs, flows, agent READMEs):
The defining sources for this schedule (task_graph.yaml and this README as provenance/chat source) are referenceable as:
`file://$(pwd)/examples/35_website_screenshot_schedule/task_graph.yaml`
`file://$(pwd)/examples/35_website_screenshot_schedule/README.md`

See updates in `packages/uri2pact/uri2pact/core.py` (markpact file:// + fragments), `uri2run/transports/paths.py`, `uri3/graph/graph_validator.py` (graph load from file://), and generator marker now emits `file://` for `markpact_readme`.
This allows uniform `file://` (and `markpact://file://...`) handling in logs, explain, touri/uri run, and agent/workflow provenance (matching the generated agents in `agents/generated/*/README.md`).

## Chat

Paste the Polish batch example from Taskinity Chat intro — line 3 resolves to
`workflow://graph/website-screenshot-schedule/dry-run` (not a per-prompt slug).
