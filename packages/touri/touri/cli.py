from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from .executor import call_uri
from .loader import load_registry
from .register import register_capability
from .validator import validate_manifest


def _print(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def cmd_list(args):
    registry = load_registry(args.registry)
    _print([m.to_dict() for m in registry])
    return 0


def cmd_validate(args):
    result = validate_manifest(args.path)
    _print(result)
    return 0 if result["ok"] else 1


def cmd_call(args):
    payload = {}
    if args.payload:
        payload = json.loads(args.payload)
    elif args.payload_file:
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    result = call_uri(args.uri, args.registry, payload=payload)
    _print(result.to_dict())
    return 0 if result.ok else 1


def cmd_register(args):
    result = register_capability(
        args.path,
        registry_root=args.registry,
        install=args.install,
    )
    _print(result)
    return 0 if result.get("ok") else 1


def build_parser():
    parser = argparse.ArgumentParser(prog="touri", description="Generic URI-to-capability manifest runtime")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="List capability manifests")
    p.add_argument(
        "registry",
        help="Directory, *.uri.capability.yaml file, or markpact://path/to/README.md",
    )
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("validate", help="Validate one capability manifest")
    p.add_argument("path")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("call", help="Call URI via matching capability manifest")
    p.add_argument("uri")
    p.add_argument(
        "--registry",
        required=True,
        help="Registry directory/file or markpact://path/to/README.md",
    )
    p.add_argument("--payload")
    p.add_argument("--payload-file")
    p.set_defaults(func=cmd_call)

    p = sub.add_parser("register", help="Validate manifest and verify uri3 explain resolution")
    p.add_argument("path", help="Capability manifest (*.uri.capability.yaml)")
    p.add_argument("--registry", required=True, help="Registry directory for touri/uri3")
    p.add_argument("--install", action="store_true", help="Copy manifest into registry directory")
    p.set_defaults(func=cmd_register)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
