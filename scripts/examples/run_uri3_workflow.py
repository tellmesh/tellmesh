#!/usr/bin/env python3
"""Run a uri3 workflow graph with the current Python interpreter."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from uri3.graph import (  # noqa: E402
    build_execution_plan,
    dry_run_workflow,
    load_workflow_graph,
    run_workflow,
    validate_workflow_graph,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Workflow graph YAML")
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--browser", default="auto")
    args = parser.parse_args(argv)

    errors = validate_workflow_graph(args.path)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2), file=sys.stderr)
        return 1

    graph = load_workflow_graph(args.path)
    if args.dry_run:
        payload = {
            "phase": "dry_run",
            "plan": build_execution_plan(graph),
            "simulation": dry_run_workflow(graph),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    result = run_workflow(
        graph,
        approve=args.approve,
        dry_run=False,
        browser_mode=args.browser,
    )
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
