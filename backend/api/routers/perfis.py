"""Profile endpoints — user profiles from 'perfis' table."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps import AuthenticatedUser, get_current_user, require_admin
from schemas.perfil import ProfileAdminUpdate, ProfileRead, ProfileUpdate
from services import profile_service

router = APIRouter(prefix="/perfis", tags=["Perfis"])


@router.get("/me", response_model=ProfileRead)
async def meu_perfil(
    user: AuthenticatedUser = Depends(get_current_user),
) -> ProfileRead:
    """Get the authenticated user's profile."""
    return profile_service.buscar_perfil(user.id)


@router.get("", response_model=list[ProfileRead])
async def listar(
    _user: AuthenticatedUser = Depends(require_admin),
) -> list[ProfileRead]:
    """List all profiles (admin only)."""
    return profile_service.listar_perfis()


@router.patch("/me", response_model=ProfileRead)
async def atualizar_proprio(
    payload: ProfileUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> ProfileRead:
    """Update the authenticated user's own profile (name only)."""
    return profile_service.atualizar_perfil(user.id, payload)


@router.patch("/{user_id}", response_model=ProfileRead)
async def atualizar_outro(
    user_id: str,
    payload: ProfileAdminUpdate,
    _user: AuthenticatedUser = Depends(require_admin),
) -> ProfileRead:
    """Admin updates another user's profile (name and/or role)."""
    return profile_service.atualizar_perfil_admin(user_id, payload)
