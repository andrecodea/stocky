"""Stock position endpoints — read-only views from 'estoque_atual'."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps import AuthenticatedUser, require_any
from schemas.produto import StockPosition
from services import product_service

router = APIRouter(prefix="/estoque", tags=["Estoque"])


@router.get("", response_model=list[StockPosition])
async def listar_estoque(
    _user: AuthenticatedUser = Depends(require_any),
) -> list[StockPosition]:
    """List current stock position for all products."""
    return product_service.listar_estoque_atual()


@router.get("/alertas", response_model=list[StockPosition])
async def listar_alertas(
    _user: AuthenticatedUser = Depends(require_any),
) -> list[StockPosition]:
    """List products below minimum stock level."""
    return product_service.listar_alertas_estoque()
