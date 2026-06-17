"""Financial service — aggregated financial summary from inventory data."""

from __future__ import annotations

from decimal import Decimal

from db.supabase import get_admin_client
from schemas.financeiro import FinancialSummary


def obter_resumo() -> FinancialSummary:
    """Calculate a financial overview from products and stock data.

    Computes:
    - Total cost of current inventory (quantity * unit cost)
    - Total potential revenue (quantity * sale price)
    - Potential margin (revenue - cost)
    - Number of products below minimum stock
    - Total product count
    - Total movement count
    """
    client = get_admin_client()

    # Fetch products
    produtos_resp = client.table("produtos").select("id, preco_custo, preco_venda").execute()
    produtos = {p["id"]: p for p in (produtos_resp.data or [])}

    # Fetch current stock
    estoque_resp = client.table("estoque_atual").select("*").execute()
    estoque_rows = estoque_resp.data or []

    # Fetch total movements count
    mov_resp = client.table("movimentacoes").select("id", count="exact").execute()
    total_movimentacoes = mov_resp.count or 0

    total_custo = Decimal("0")
    total_valor = Decimal("0")
    abaixo_minimo = 0

    for row in estoque_rows:
        pid = row["produto_id"]
        quantidade = int(row.get("quantidade_atual") or 0)
        minimo = int(row.get("estoque_minimo") or 0)

        if quantidade < minimo:
            abaixo_minimo += 1

        produto = produtos.get(pid, {})
        custo = Decimal(str(produto.get("preco_custo") or 0))
        venda = Decimal(str(produto.get("preco_venda") or 0))

        total_custo += custo * quantidade
        total_valor += venda * quantidade

    return FinancialSummary(
        total_custo_estoque=total_custo,
        total_valor_estoque=total_valor,
        margem_potencial=total_valor - total_custo,
        produtos_abaixo_minimo=abaixo_minimo,
        total_produtos=len(produtos),
        total_movimentacoes=total_movimentacoes,
    )
