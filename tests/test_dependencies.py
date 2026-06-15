"""Runtime dependency sanity checks."""

from __future__ import annotations

from importlib.metadata import version


def test_typer_bundled_click_is_complete():
    """Typer >=0.26 vendors click as typer._click; partial installs break all CLIs."""
    import typer._click.decorators  # noqa: F401

    installed = version("typer")
    major, minor, *_ = (int(part) for part in installed.split(".")[:2])
    assert (major, minor) >= (0, 26), f"typer {installed} too old; need >=0.26.7"
