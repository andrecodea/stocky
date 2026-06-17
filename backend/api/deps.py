"""FastAPI dependencies for authentication and authorization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from fastapi import Depends, HTTPException, Header

from db.supabase import get_admin_client, get_anon_client


@dataclass(frozen=True)
class AuthenticatedUser:
    """Represents the currently authenticated user."""

    id: str
    role: str  # 'operador' | 'admin'
    nome: str


async def get_current_user(
    authorization: str | None = Header(default=None, description="Bearer <JWT token>"),
) -> AuthenticatedUser:
    """Validate the Supabase Auth token and return the authenticated user.

    Raises:
        HTTPException 401: If the token is missing, invalid, or if the user
            profile is not found.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token invalido")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token invalido")

    token = parts[1]

    try:
        auth_response = get_anon_client().auth.get_user(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalido")

    auth_user = getattr(auth_response, "user", None)
    user_id: str | None = getattr(auth_user, "id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token invalido: sem identificador de usuario")

    response = (
        get_admin_client()
        .table("perfis")
        .select("id, nome, role")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )
    rows = response.data or []
    if not rows:
        raise HTTPException(status_code=401, detail="Perfil de usuario nao encontrado")

    profile = rows[0]
    return AuthenticatedUser(
        id=profile["id"],
        role=profile["role"],
        nome=profile["nome"],
    )


def require_role(*allowed_roles: str) -> Callable:
    """Dependency factory that restricts access to specific roles.

    Usage::

        @router.get("/admin-only")
        async def admin_endpoint(user: AuthenticatedUser = Depends(require_admin)):
            ...
    """

    async def _check_role(
        user: AuthenticatedUser = Depends(get_current_user),
    ) -> AuthenticatedUser:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Acesso negado para o papel '{user.role}'",
            )
        return user

    return _check_role


require_admin = require_role("admin")
require_any = require_role("operador", "admin")
