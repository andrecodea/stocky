"""Financial summary endpoints (admin only)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps import AuthenticatedUser, require_admin
from schemas.financeiro import FinancialSummary
from services import financial_service

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])


@router.get("/resumo", response_model=FinancialSummary)
async def resumo(
    _user: AuthenticatedUser = Depends(require_admin),
) -> FinancialSummary:
    """Get aggregated financial summary of inventory (admin only)."""
    return financial_service.obter_resumo()
