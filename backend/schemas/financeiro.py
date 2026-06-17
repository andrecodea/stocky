"""Financial summary schemas."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class FinancialSummary(BaseModel):
    """Aggregated financial overview of the inventory."""

    total_custo_estoque: Decimal
    total_valor_estoque: Decimal
    margem_potencial: Decimal
    produtos_abaixo_minimo: int
    total_produtos: int
    total_movimentacoes: int
