"""Tests for touri explain command."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from touri.cli import cmd_explain


class _Args:
    uri = "weather://forecast/Gdansk/14/html"
    registry = ""


def test_touri_explain_delegates_to_uri3(repo_root: Path):
    args = _Args()
    args.registry = str(repo_root / "examples" / "20_touri_capabilities")
    buffer = StringIO()
    with patch("sys.stdout", buffer):
        code = cmd_explain(args)
    assert code == 0
    payload = json.loads(buffer.getvalue())
    assert payload["matched_registry"] == "touri"
    assert payload["capability"] == "weather.forecast.html"
