"""Profile schemas aligned with the 'perfis' table."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProfileRead(BaseModel):
    """Full profile representation."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    role: str
    criado_em: datetime | None = None


class ProfileUpdate(BaseModel):
    """Payload for a user updating their own profile.

    Role cannot be self-changed — that requires admin action.
    """

    nome: str = Field(..., min_length=1)


class ProfileAdminUpdate(BaseModel):
    """Payload for admin updating any user's profile."""

    nome: str | None = Field(default=None, min_length=1)
    role: str | None = Field(default=None, pattern=r"^(operador|admin)$")
