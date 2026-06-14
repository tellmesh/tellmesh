# External Packages And Local Integrations

Local audit date: 2026-06-14.

This document tracks packages from neighboring `semcod/*` and `wronai/*`
repositories that are relevant to `hypervisor`.

## Current Dependency Boundary

`hypervisor` does not currently have runtime dependencies on:

```txt
markpact
pactown
iterun
intract
nlp2dsl
semcod/nlp2uri
```

The active runtime packages are workspace packages in this repository:

```txt
uri3
nl2uri
uri2flow
uri2ops
touri
resource-agent-hypervisor
resource-agent-factory
```

External `semcod/*` packages used directly by this repo are development tools:

```txt
goal
costs
pfix
```

The `markpact://` support in `touri` and `uri2flow` is intentionally thin. It
parses fenced `markpact:*` code blocks from README files and validates the
resulting manifest or compact flow locally. It does not call the `markpact`
runtime.

## Version Snapshot

| Package | Role | Local repo | Installed metadata | CLI observed | Action |
|---------|------|------------|--------------------|--------------|--------|
| `markpact` | README contract runtime; source format for `markpact://` | `0.1.42` | `0.1.42` | `0.1.42` | OK now |
| `pactown` | Workspace discovery/orchestration for many markpact services | `0.1.173` | `0.1.173` | `0.1.156` | Update CLI wrapper before `pactown://` integration |
| `iterun` | execute -> verify -> repair loop | `0.1.12` | `0.1.12` | available | OK now; adapter needed later |
| `intract` | intent contracts and policy/quality gate | `0.5.13` | `0.5.6` | `0.5.13` | Align environment before policy gate work |
| `nlp2dsl` | conversation flow and Domain DSL generator | `0.0.40` | `0.0.7` | demo CLI only | Update before domain-pack bridge work |
| `semcod/nlp2uri` | desktop/OS URI planner | `0.4.15` | `0.4.13` | `0.4.15` | Keep separate from `hypervisor/packages/nl2uri` |
| `goal` | dev tool | `2.1.247` | `2.1.246` | `2.1.247` | Prefer `uv run goal` or resync |
| `costs` | dev cost tracker | `0.1.51` | `0.1.51` | `0.1.39` | Global wrapper is stale |
| `pfix` | dev repair tool | `0.1.73` | `0.1.73` | `0.1.72` | Global wrapper is slightly stale |

The CLI column may differ from installed Python metadata because some commands
are resolved from `~/.local/bin` while others are resolved from the active
virtual environment. Prefer `uv run ...` from this repository when validating
tool behavior.

## Recommended Integration Order

```txt
1. markpact:// loader for touri              done
2. markpact:// flow loader for uri2flow      done
3. uri3 scan pactown://...                   next
4. nlp2dsl -> domain pack / markpact export  later
5. iterun retry/repair for uri3 workflow     later
6. intract policy gate                       later
```

## Required Package Work

### pactown

Before implementing `uri3 scan pactown://...`, choose one stable integration
surface:

```txt
preferred: Python API using pactown.generator.scan_folder
alternative: pactown scan --json
```

The current CLI help exposes `pactown scan FOLDER` but no JSON output. A JSON
mode would make `uri3` integration easier to test and less dependent on text
formatting.

### markpact

No update is required for the current `markpact://` loaders.

Optional later improvement:

```txt
markpact.parse_blocks(markdown, kind="capability" | "flow")
```

That would let `touri` and `uri2flow` share a public parser instead of each
package keeping a small local fenced-block parser.

### nlp2dsl

Update or install editable only when starting the domain-pack bridge:

```txt
nlp2dsl conversation -> domain.dsl.yaml -> markpact README -> hypervisor domain pack
```

Do not use `nlp2dsl` as a replacement for `hypervisor/packages/nl2uri`.

### intract

Use `intract` as a policy/quality gate, not as an interactive missing-fields
conversation loop. The conversation loop belongs in `nlp2dsl`.

### semcod/nlp2uri

Keep separate from `hypervisor/packages/nl2uri`:

```txt
semcod/nlp2uri          -> desktop/OS URI planning
hypervisor/packages/nl2uri -> agent/workflow URI plans
```

Only use `semcod/nlp2uri` as an optional source of `uri2ops` desktop ideas.

### iterun

No package update is required now. The missing piece is a bounded adapter:

```txt
uri3 run-workflow --iterun
  -> run
  -> verify
  -> collect logs/artifacts
  -> repair proposal
  -> rerun with max iterations and policy gate
```

## Environment Hygiene

Use repository-local commands when possible:

```bash
uv sync --extra dev
uv run python -m pytest -q
uv run goal --version
uv run pfix version
uv run costs --help
```

If a global wrapper must be used, verify it first:

```bash
command -v pactown markpact iterun intract nlp2uri goal costs pfix
pactown --version
markpact --version
```

Do not assume local dirty checkouts are publishable versions. Several neighboring
repositories had uncommitted changes during the 2026-06-14 audit.
