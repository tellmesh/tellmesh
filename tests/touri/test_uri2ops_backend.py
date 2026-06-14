"""Tests for touri uri2ops backend and redaction."""

from __future__ import annotations

from pathlib import Path

import yaml

from touri.executor import call_uri


def test_uri2ops_backend_open_page(repo_root: Path):
    registry = repo_root / "examples" / "20_touri_capabilities"
    result = call_uri(
        "browser://touri/mock/page/open",
        registry,
        payload={"url": "http://localhost:8101/health"},
        context={"root": repo_root},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["capability"] == "browser.open.page"
    assert payload["backend"] == "uri2ops"


def test_redaction_masks_secret_payload_fields(tmp_path: Path):
    manifest = {
        "version": 1,
        "capability": {
            "id": "secret.echo",
            "scheme": "echo",
            "uri_template": "echo://{name}",
            "operation": "read",
            "kind": "query",
        },
        "backend": {"type": "mock"},
        "policy": {"redact_secrets": True},
    }
    path = tmp_path / "secret.uri.capability.yaml"
    path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    result = call_uri("echo://user", tmp_path, payload={"api_key": "secret-value", "name": "user"})
    payload = result.to_dict()
    assert payload["data"]["payload"]["name"] == "user"
    assert payload["data"]["payload"]["api_key"] == "[REDACTED]"
