# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
# Contract hash: sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda

from __future__ import annotations

from fastapi import FastAPI

try:
    from .routes import router
except ImportError:  # standalone rsync package on remote host
    from routes import router

app = FastAPI(
    title="generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent",
    version="0.1.0",
    description='generuj mape pogody dwa tygodnie do przodu w html',
)
app.include_router(router)
