"""AI insight schemas aligned with the 'ai_logs' table."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

InsightType = Literal[
    "estoque",
    "financeiro",
    "comercial",
    "logistica",
    "supply_chain",
    "geral",
]
InsightSeverity = Literal["info", "atencao", "critica"]
InsightAudience = Literal["operador", "admin", "ambos"]


class AiLogCreate(BaseModel):
    """Structured payload persisted by AI agents or scheduled jobs."""

    tipo: InsightType
    titulo: str = Field(..., min_length=1)
    resumo: str = Field(..., min_length=1)
    conteudo: dict[str, Any] = Field(default_factory=dict)
    fontes: list[dict[str, Any]] = Field(default_factory=list)
    severidade: InsightSeverity = "info"
    audiencia: InsightAudience = "ambos"
    agente: str | None = None


class AiLogRead(BaseModel):
    """AI insight representation exposed to mobile and web clients."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    tipo: str
    titulo: str
    resumo: str
    conteudo: dict[str, Any] = Field(default_factory=dict)
    fontes: list[dict[str, Any]] = Field(default_factory=list)
    severidade: str = "info"
    audiencia: str = "ambos"
    agente: str | None = None
    criado_em: datetime | None = None
