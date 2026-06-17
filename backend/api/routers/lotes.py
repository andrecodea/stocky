"""Batch (lote) endpoints — CRUD on 'lotes' table."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api.deps import AuthenticatedUser, require_admin, require_any
from schemas.lote import BatchCreate, BatchRead, BatchUpdate
from services import batch_service

router = APIRouter(prefix="/lotes", tags=["Lotes"])


@router.get("", response_model=list[BatchRead])
async def listar(
    produto_id: str | None = Query(default=None, description="Filter by product ID"),
    _user: AuthenticatedUser = Depends(require_any),
) -> list[BatchRead]:
    """List batches, optionally filtered by product."""
    return batch_service.listar_lotes(produto_id=produto_id)


@router.get("/{lote_id}", response_model=BatchRead)
async def buscar(
    lote_id: str,
    _user: AuthenticatedUser = Depends(require_any),
) -> BatchRead:
    """Get a batch by ID."""
    return batch_service.buscar_lote(lote_id)


@router.post("", response_model=BatchRead, status_code=201)
async def criar(
    payload: BatchCreate,
    _user: AuthenticatedUser = Depends(require_admin),
) -> BatchRead:
    """Create a new batch (admin only)."""
    return batch_service.criar_lote(payload)


@router.patch("/{lote_id}", response_model=BatchRead)
async def atualizar(
    lote_id: str,
    payload: BatchUpdate,
    _user: AuthenticatedUser = Depends(require_admin),
) -> BatchRead:
    """Update a batch (admin only)."""
    return batch_service.atualizar_lote(lote_id, payload)


@router.delete("/{lote_id}", status_code=204)
async def deletar(
    lote_id: str,
    _user: AuthenticatedUser = Depends(require_admin),
) -> None:
    """Delete a batch (admin only)."""
    batch_service.deletar_lote(lote_id)
