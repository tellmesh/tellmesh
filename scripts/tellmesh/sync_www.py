#!/usr/bin/env python3
"""Sync hypervisor static www/ assets into tellmesh/www (canonical product site repo)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HYPERVISOR_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TARGET = HYPERVISOR_ROOT.parent.parent / "tellmesh" / "www"

# Deploy glue stays in the hypervisor repo.
EXCLUDE = {
    "Dockerfile",
    "docker-compose.yml",
}


def sync_www(*, source: Path, target: Path, dry_run: bool = False) -> list[str]:
    if not source.is_dir():
        raise SystemExit(f"source www not found: {source}")
    target.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source)
        if rel.parts and rel.parts[0] in EXCLUDE:
            continue
        if rel.name in EXCLUDE:
            continue
        dest = target / rel
        if dry_run:
            copied.append(str(rel))
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        copied.append(str(rel))
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"tellmesh/www checkout (default: {DEFAULT_TARGET})",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true", help="exit 1 if target differs")
    args = parser.parse_args()

    source = HYPERVISOR_ROOT / "www"
    target = args.target.resolve()

    if args.check:
        tmp = target.parent / ".www-sync-check"
        if tmp.exists():
            shutil.rmtree(tmp)
        sync_www(source=source, target=tmp, dry_run=False)
        diff = subprocess.run(
            ["diff", "-qr", str(tmp), str(target)],
            capture_output=True,
            text=True,
        )
        shutil.rmtree(tmp, ignore_errors=True)
        if diff.returncode != 0:
            sys.stderr.write(diff.stdout)
            sys.stderr.write(diff.stderr)
            return 1
        print(f"OK tellmesh/www matches hypervisor/www ({target})")
        return 0

    files = sync_www(source=source, target=target, dry_run=args.dry_run)
    action = "would copy" if args.dry_run else "copied"
    print(f"{action} {len(files)} files -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
