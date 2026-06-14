"""Fixture-backed capability tests for weather.forecast.html."""

from __future__ import annotations

from pathlib import Path


FIXTURE_KINDS = ("good", "irrelevant", "blocked", "fallback")


def test_weather_forecast_fixtures_exist(repo_root: Path):
    base = repo_root / "tests" / "capabilities" / "weather_forecast" / "fixtures"
    for kind in FIXTURE_KINDS:
        files = list((base / kind).glob("*.html"))
        assert files, f"missing html fixture under {kind}"


def test_good_fixture_contains_expected_marker(repo_root: Path):
    path = repo_root / "tests" / "capabilities" / "weather_forecast" / "fixtures" / "good" / "forecast.html"
    content = path.read_text(encoding="utf-8")
    assert "Gdansk" in content
    assert "ok" in content
