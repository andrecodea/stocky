"""Batch service — CRUD operations on the 'lotes' table."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from api.exceptions import NotFoundError
from db.supabase import get_admin_client
from schemas.lote import BatchCreate, BatchRead, BatchUpdate

_TABLE = "lotes"


def _serialize(payload: dict) -> dict:
    """Convert Python types to JSON-safe values for Supabase."""
    out: dict = {}
    for key, value in payload.items():
        if isinstance(value, Decimal):
            out[key] = float(value)
        elif isinstance(value, (datetime, date)):
            out[key] = value.isoformat()
        else:
            out[key] = value
    return out


def listar_lotes(produto_id: str | None = None) -> list[BatchRead]:
    """List batches, optionally filtered by product."""
    query = get_admin_client().table(_TABLE).select("*").order("criado_em", desc=True)
    if produto_id:
        query = query.eq("produto_id", produto_id)
    response = query.execute()
    return [BatchRead.model_validate(row) for row in response.data or []]


def buscar_lote(lote_id: str) -> BatchRead:
    """Fetch a single batch by UUID. Raises NotFoundError if missing."""
    response = (
        get_admin_client()
        .table(_TABLE)
        .select("*")
        .eq("id", lote_id)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Lote", lote_id)
    return BatchRead.model_validate(rows[0])


def criar_lote(data: BatchCreate) -> BatchRead:
    """Insert a new batch."""
    # Validate product exists
    from services.product_service import buscar_produto

    buscar_produto(data.produto_id)  # raises NotFoundError

    payload = _serialize(data.model_dump(exclude_none=True))
    response = get_admin_client().table(_TABLE).insert(payload).execute()
    return BatchRead.model_validate(response.data[0])


def atualizar_lote(lote_id: str, data: BatchUpdate) -> BatchRead:
    """Partially update a batch."""
    buscar_lote(lote_id)  # raises NotFoundError

    fields = {name: getattr(data, name) for name in data.model_fields_set}
    if not fields:
        return buscar_lote(lote_id)

    payload = _serialize(fields)
    response = (
        get_admin_client()
        .table(_TABLE)
        .update(payload)
        .eq("id", lote_id)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Lote", lote_id)
    return BatchRead.model_validate(rows[0])


def deletar_lote(lote_id: str) -> bool:
    """Delete a batch by UUID."""
    buscar_lote(lote_id)  # raises NotFoundError
    response = get_admin_client().table(_TABLE).delete().eq("id", lote_id).execute()
    return bool(response.data)
