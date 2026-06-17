"""AI insight service for persisted structured logs."""

from __future__ import annotations

from typing import Any

from db.supabase import get_admin_client
from schemas.ai import AiLogCreate, AiLogRead

_TABLE = "ai_logs"
_FIELDS = (
    "id,tipo,titulo,resumo,conteudo,fontes,severidade,audiencia,agente,criado_em"
)


def listar_insights(
    *,
    role: str,
    tipo: str | None = None,
    limit: int = 50,
    client: Any | None = None,
) -> list[AiLogRead]:
    """List persisted AI insights visible to the authenticated role."""
    db = client or get_admin_client()
    query = db.table(_TABLE).select(_FIELDS).order("criado_em", desc=True).limit(limit)

    if tipo:
        query = query.eq("tipo", tipo)

    if role != "admin":
        query = query.in_("audiencia", ["operador", "ambos"])

    response = query.execute()
    return [AiLogRead.model_validate(row) for row in response.data or []]


def criar_ai_log(data: AiLogCreate, *, client: Any | None = None) -> AiLogRead:
    """Persist a structured AI log and return the stored row."""
    db = client or get_admin_client()
    payload = data.model_dump(exclude_none=True)
    response = db.table(_TABLE).insert(payload).execute()
    return AiLogRead.model_validate(response.data[0])
