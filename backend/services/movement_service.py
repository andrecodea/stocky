"""Movement service — CRUD operations on the 'movimentacoes' table."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from api.exceptions import NotFoundError
from db.supabase import get_admin_client
from schemas.movimentacao import MovementCreate, MovementRead

_TABLE = "movimentacoes"


def _serialize(payload: dict) -> dict:
    """Convert Python types to JSON-safe values for Supabase."""
    out: dict = {}
    for key, value in payload.items():
        if isinstance(value, Decimal):
            out[key] = float(value)
        elif isinstance(value, datetime):
            out[key] = value.isoformat()
        elif hasattr(value, "value"):  # Enum
            out[key] = value.value
        else:
            out[key] = value
    return out


def listar_movimentacoes(
    produto_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[MovementRead]:
    """List movements with optional product filter and pagination."""
    query = (
        get_admin_client()
        .table(_TABLE)
        .select("*")
        .order("criado_em", desc=True)
        .range(offset, offset + limit - 1)
    )
    if produto_id:
        query = query.eq("produto_id", produto_id)
    response = query.execute()
    return [MovementRead.model_validate(row) for row in response.data or []]


def buscar_movimentacao(mov_id: str) -> MovementRead:
    """Fetch a single movement by UUID. Raises NotFoundError if missing."""
    response = (
        get_admin_client()
        .table(_TABLE)
        .select("*")
        .eq("id", mov_id)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Movimentação", mov_id)
    return MovementRead.model_validate(rows[0])


def criar_movimentacao(data: MovementCreate, usuario_id: str) -> MovementRead:
    """Insert a new stock movement, binding it to the authenticated user."""
    # Validate that the product exists
    from services.product_service import buscar_produto

    buscar_produto(data.produto_id)  # raises NotFoundError

    # Validate batch if provided
    if data.lote_id:
        from services.batch_service import buscar_lote

        buscar_lote(data.lote_id)  # raises NotFoundError

    payload = _serialize(data.model_dump(exclude_none=True))
    payload["usuario_id"] = usuario_id

    response = get_admin_client().table(_TABLE).insert(payload).execute()
    return MovementRead.model_validate(response.data[0])
