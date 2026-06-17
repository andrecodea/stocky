"""Product schemas aligned with the 'produtos' table."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    """Payload for creating a new product.

    Only 'nome' is required. Other fields have defaults in the database.
    """

    nome: str = Field(..., min_length=1)
    sku: str | None = None
    descricao: str | None = None
    preco_custo: Decimal = Field(default=Decimal("0"), ge=0)
    preco_venda: Decimal = Field(default=Decimal("0"), ge=0)
    unidade: str = "un"
    estoque_minimo: int = Field(default=0, ge=0)
    foto_url: str | None = None


class ProductUpdate(BaseModel):
    """Partial update payload for a product.

    Only explicitly set fields are persisted, detected via `model_fields_set`.
    """

    nome: str | None = Field(default=None, min_length=1)
    sku: str | None = None
    descricao: str | None = None
    preco_custo: Decimal | None = Field(default=None, ge=0)
    preco_venda: Decimal | None = Field(default=None, ge=0)
    unidade: str | None = None
    estoque_minimo: int | None = Field(default=None, ge=0)
    foto_url: str | None = None


class ProductRead(BaseModel):
    """Full product representation as persisted in the database."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    sku: str | None = None
    descricao: str | None = None
    preco_custo: Decimal
    preco_venda: Decimal
    unidade: str
    estoque_minimo: int
    foto_url: str | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None


class StockPosition(BaseModel):
    """Product enriched with current stock position from 'estoque_atual' view."""

    model_config = ConfigDict(from_attributes=True)

    produto_id: str
    nome: str
    sku: str | None = None
    unidade: str
    estoque_minimo: int
    quantidade_atual: int
    abaixo_minimo: bool
