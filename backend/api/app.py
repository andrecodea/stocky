"""Stocky FastAPI application entrypoint."""

# ruff: noqa: E402

from __future__ import annotations

import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the backend directory is on the Python path
_backend_dir = Path(__file__).resolve().parent.parent
if str(_backend_dir) not in sys.path:
    sys.path.insert(0, str(_backend_dir))

from dotenv import load_dotenv

load_dotenv(Path(_backend_dir).parent / ".env")

from config import settings
from api.exceptions import register_exception_handlers
from api.routers import (
    ai,
    auth,
    estoque,
    financeiro,
    lotes,
    movimentacoes,
    perfis,
    produtos,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stocky — Inventory Management API",
    description="Backend API para gerenciamento inteligente de estoque.",
    version="0.1.0",
)

# --- Middleware -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Exception handlers ---------------------------------------------------
register_exception_handlers(app)

# --- Routers --------------------------------------------------------------
app.include_router(auth.router)
app.include_router(ai.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(movimentacoes.router)
app.include_router(lotes.router)
app.include_router(perfis.router)
app.include_router(financeiro.router)


# --- Health / Ping --------------------------------------------------------
@app.get("/ping", tags=["Health"])
def ping() -> dict:
    """Simple liveness check."""
    return {"pong": True}


@app.get("/health", include_in_schema=False)
def health() -> dict:
    """Health check for load balancers and monitoring."""
    return {"status": "ok"}


# --- Entrypoint -----------------------------------------------------------
if __name__ == "__main__":
    logger.info("--- Stocky API starting ---")
    uvicorn.run(
        "api.app:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True,
    )
