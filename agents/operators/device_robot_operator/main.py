"""Device and robot operator agent — isolated uri2ops runtime on :8792."""

from __future__ import annotations

from agents.operators.operator_runtime import create_operator_app

app = create_operator_app(
    __file__,
    default_port=8792,
    title="device-robot-operator",
)
