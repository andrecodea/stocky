"""Movement (movimentacao) schemas aligned with the 'movimentacoes' table."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TipoMovimentacao(str, Enum):
    """Stock movement types matching the 'tipo_movimentacao' SQL enum."""

    ENTRADA = "entrada"
    SAIDA = "saida"
    AJUSTE = "ajuste"


class MovementCreate(BaseModel):
    """Payload for creating a stock movement.

    The 'usuario_id' is injected from the authenticated user, not from the client.
    """

    produto_id: str
    tipo: TipoMovimentacao
    quantidade: int = Field(..., gt=0)
    lote_id: str | None = None
    custo_unitario: Decimal | None = Field(default=None, ge=0)
    observacao: str | None = None


class MovementRead(BaseModel):
    """Full movement representation as persisted."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    produto_id: str
    lote_id: str | None = None
    tipo: str
    quantidade: int
    custo_unitario: Decimal | None = None
    observacao: str | None = None
    usuario_id: str | None = None
    criado_em: datetime | None = None


class MovementWithProduct(BaseModel):
    """Movement enriched with product name for listing views."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    produto_id: str
    produto_nome: str
    tipo: str
    quantidade: int
    custo_unitario: Decimal | None = None
    observacao: str | None = None
    usuario_id: str | None = None
    criado_em: datetime | None = None
