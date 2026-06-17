"""Batch (lote) schemas aligned with the 'lotes' table."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BatchCreate(BaseModel):
    """Payload for creating a product batch."""

    produto_id: str
    numero_lote: str | None = None
    data_validade: date | None = None
    fornecedor: str | None = None
    custo_unitario: Decimal | None = Field(default=None, ge=0)


class BatchUpdate(BaseModel):
    """Partial update payload for a batch."""

    numero_lote: str | None = None
    data_validade: date | None = None
    fornecedor: str | None = None
    custo_unitario: Decimal | None = Field(default=None, ge=0)


class BatchRead(BaseModel):
    """Full batch representation as persisted."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    produto_id: str
    numero_lote: str | None = None
    data_validade: date | None = None
    fornecedor: str | None = None
    custo_unitario: Decimal | None = None
    criado_em: datetime | None = None
