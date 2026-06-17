"""AI insight endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from api.deps import AuthenticatedUser, require_admin, require_any
from schemas.ai import AiLogCreate, AiLogRead
from services import ai_insight_service

router = APIRouter(prefix="/ai", tags=["IA"])


@router.get("/insights", response_model=list[AiLogRead])
async def listar_insights(
    tipo: str | None = Query(default=None, description="Filter by insight type"),
    limit: int = Query(default=50, ge=1, le=100),
    user: AuthenticatedUser = Depends(require_any),
) -> list[AiLogRead]:
    """List stored AI insights visible to the current user's role."""
    return ai_insight_service.listar_insights(
        role=user.role,
        tipo=tipo,
        limit=limit,
    )


@router.post("/insights", response_model=AiLogRead, status_code=201)
async def criar_insight(
    payload: AiLogCreate,
    _user: AuthenticatedUser = Depends(require_admin),
) -> AiLogRead:
    """Persist a structured AI insight (admin/internal workflow)."""
    return ai_insight_service.criar_ai_log(payload)
