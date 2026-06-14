"""Tests for touri register + uri3 explain integration."""

from __future__ import annotations

from pathlib import Path

from touri.register import register_capability, sample_uri_from_template


def test_sample_uri_from_template():
    uri = sample_uri_from_template("weather://forecast/{place}/{days}/html")
    assert uri == "weather://forecast/Gdansk/14/html"


def test_register_capability_matches_uri3_explain(repo_root: Path, tmp_path: Path):
    manifest = repo_root / "examples" / "20_touri_capabilities" / "weather_forecast.uri.capability.yaml"
    result = register_capability(manifest, registry_root=tmp_path, install=True, root=repo_root)
    assert result["ok"] is True
    assert result["capability"] == "weather.forecast.html"
    assert result["explain"]["matched_registry"] == "touri"
    assert (tmp_path / manifest.name).is_file()
