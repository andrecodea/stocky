"""Movement endpoints — CRUD on 'movimentacoes' table."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api.deps import AuthenticatedUser, require_any
from schemas.movimentacao import MovementCreate, MovementRead
from services import movement_service

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])


@router.get("", response_model=list[MovementRead])
async def listar(
    produto_id: str | None = Query(default=None, description="Filter by product ID"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    _user: AuthenticatedUser = Depends(require_any),
) -> list[MovementRead]:
    """List stock movements with optional filtering and pagination."""
    return movement_service.listar_movimentacoes(
        produto_id=produto_id, limit=limit, offset=offset
    )


@router.get("/{mov_id}", response_model=MovementRead)
async def buscar(
    mov_id: str,
    _user: AuthenticatedUser = Depends(require_any),
) -> MovementRead:
    """Get a movement by ID."""
    return movement_service.buscar_movimentacao(mov_id)


@router.post("", response_model=MovementRead, status_code=201)
async def criar(
    payload: MovementCreate,
    user: AuthenticatedUser = Depends(require_any),
) -> MovementRead:
    """Create a new stock movement.

    The authenticated user's ID is automatically bound to the movement.
    """
    return movement_service.criar_movimentacao(payload, usuario_id=user.id)
