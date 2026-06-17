"""Profile service — operations on the 'perfis' table."""

from __future__ import annotations

from api.exceptions import NotFoundError
from db.supabase import get_admin_client
from schemas.perfil import ProfileAdminUpdate, ProfileRead, ProfileUpdate

_TABLE = "perfis"


def buscar_perfil(user_id: str) -> ProfileRead:
    """Fetch a user profile by ID. Raises NotFoundError if missing."""
    response = (
        get_admin_client()
        .table(_TABLE)
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Perfil", user_id)
    return ProfileRead.model_validate(rows[0])


def listar_perfis() -> list[ProfileRead]:
    """List all user profiles ordered by name."""
    response = get_admin_client().table(_TABLE).select("*").order("nome").execute()
    return [ProfileRead.model_validate(row) for row in response.data or []]


def atualizar_perfil(user_id: str, data: ProfileUpdate) -> ProfileRead:
    """Update a user's own profile (name only)."""
    buscar_perfil(user_id)  # raises NotFoundError

    response = (
        get_admin_client()
        .table(_TABLE)
        .update({"nome": data.nome})
        .eq("id", user_id)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Perfil", user_id)
    return ProfileRead.model_validate(rows[0])


def atualizar_perfil_admin(user_id: str, data: ProfileAdminUpdate) -> ProfileRead:
    """Admin updates any user's profile, including role."""
    buscar_perfil(user_id)  # raises NotFoundError

    fields = {name: getattr(data, name) for name in data.model_fields_set}
    if not fields:
        return buscar_perfil(user_id)

    response = (
        get_admin_client()
        .table(_TABLE)
        .update(fields)
        .eq("id", user_id)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise NotFoundError("Perfil", user_id)
    return ProfileRead.model_validate(rows[0])
