"""Product service — CRUD operations on the 'produtos' table."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from api.exceptions import ConflictError, NotFoundError
from db.supabase import get_admin_client
from schemas.produto import ProductCreate, ProductRead, ProductUpdate, StockPosition

_TABLE = "produtos"
_VIEW_ESTOQUE = "estoque_atual"


def _serialize(payload: dict) -> dict:
    """Convert Python types (Decimal, datetime, date) to JSON-safe values."""
    out: dict = {}
    for key, value in payload.items():
        if isinstance(value, Decimal):
            out[key] = float(value)
        elif isinstance(value, datetime):
            out[key] = value.isoformat()
        else:
            out[key] = value
    return out


def listar_produtos() -> list[ProductRead]:
    """Return all products ordered by name."""
    response = get_admin_client().table(_TABLE).select("*").order("nome").execute()
    return [ProductRead.model_validate(row) for row in response.data or []]


def buscar_produto(produto_id: str) -> ProductRead:
    """Fetch a single product by UUID. Raises NotFoundError if missing."""
    response = (
        get_admin_client()
        .table(_TABLE)
        .select("*")
        .eq("id", produto_id)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Produto", produto_id)
    return ProductRead.model_validate(rows[0])


def buscar_produto_por_sku(sku: str) -> ProductRead | None:
    """Fetch a product by SKU. Returns None if not found."""
    response = (
        get_admin_client()
        .table(_TABLE)
        .select("*")
        .eq("sku", sku)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if not rows:
        return None
    return ProductRead.model_validate(rows[0])


def criar_produto(data: ProductCreate) -> ProductRead:
    """Insert a new product. Raises ConflictError on duplicate SKU."""
    if data.sku:
        existing = buscar_produto_por_sku(data.sku)
        if existing:
            raise ConflictError(f"SKU '{data.sku}' já está em uso")

    payload = _serialize(data.model_dump(exclude_none=True))
    response = get_admin_client().table(_TABLE).insert(payload).execute()
    return ProductRead.model_validate(response.data[0])


def atualizar_produto(produto_id: str, data: ProductUpdate) -> ProductRead:
    """Partially update a product. Only explicitly set fields are sent."""
    # Ensure the product exists
    buscar_produto(produto_id)

    fields = {name: getattr(data, name) for name in data.model_fields_set}
    if not fields:
        return buscar_produto(produto_id)

    # Check SKU uniqueness if changing SKU
    if "sku" in fields and fields["sku"] is not None:
        existing = buscar_produto_por_sku(fields["sku"])
        if existing and existing.id != produto_id:
            raise ConflictError(f"SKU '{fields['sku']}' já está em uso")

    payload = _serialize(fields)
    response = (
        get_admin_client()
        .table(_TABLE)
        .update(payload)
        .eq("id", produto_id)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Produto", produto_id)
    return ProductRead.model_validate(rows[0])


def deletar_produto(produto_id: str) -> bool:
    """Delete a product by UUID. Returns True if deleted."""
    buscar_produto(produto_id)  # raises NotFoundError if missing
    response = (
        get_admin_client().table(_TABLE).delete().eq("id", produto_id).execute()
    )
    return bool(response.data)


def listar_estoque_atual() -> list[StockPosition]:
    """List current stock position from the 'estoque_atual' view."""
    response = (
        get_admin_client().table(_VIEW_ESTOQUE).select("*").order("nome").execute()
    )
    result: list[StockPosition] = []
    for row in response.data or []:
        quantidade = row.get("quantidade_atual") or 0
        minimo = row.get("estoque_minimo") or 0
        result.append(
            StockPosition(
                produto_id=row["produto_id"],
                nome=row["nome"],
                sku=row.get("sku"),
                unidade=row.get("unidade", "un"),
                estoque_minimo=minimo,
                quantidade_atual=quantidade,
                abaixo_minimo=quantidade < minimo,
            )
        )
    return result


def listar_alertas_estoque() -> list[StockPosition]:
    """Return only products below minimum stock level."""
    return [p for p in listar_estoque_atual() if p.abaixo_minimo]
