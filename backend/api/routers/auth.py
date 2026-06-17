"""Authentication router — login and signup via Supabase Auth."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from db.supabase import get_anon_client, get_admin_client
from schemas.auth import AuthResponse, LoginRequest, SignupRequest, UserInfo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=AuthResponse)
async def login(payload: LoginRequest) -> AuthResponse:
    """Authenticate a user and return tokens + profile."""
    try:
        result = get_anon_client().auth.sign_in_with_password(
            {"email": payload.email, "password": payload.senha}
        )
    except Exception as exc:
        logger.warning("Login failed for %s: %s", payload.email, exc)
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    session = result.session
    user = result.user

    if not session or not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Fetch profile for role info
    profile_resp = (
        get_admin_client()
        .table("perfis")
        .select("nome, role")
        .eq("id", user.id)
        .limit(1)
        .execute()
    )
    profile = (profile_resp.data or [{}])[0]

    return AuthResponse(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        user=UserInfo(
            id=user.id,
            email=user.email or payload.email,
            nome=profile.get("nome", "Usuário"),
            role=profile.get("role", "operador"),
        ),
    )


@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(payload: SignupRequest) -> AuthResponse:
    """Register a new user. Profile is created automatically via DB trigger."""
    try:
        result = get_anon_client().auth.sign_up(
            {
                "email": payload.email,
                "password": payload.senha,
                "options": {"data": {"nome": payload.nome}},
            }
        )
    except Exception as exc:
        logger.warning("Signup failed for %s: %s", payload.email, exc)
        raise HTTPException(status_code=400, detail="Erro ao criar conta")

    session = result.session
    user = result.user

    if not user:
        raise HTTPException(status_code=400, detail="Erro ao criar conta")

    # If email confirmation is required, session may be None
    access_token = session.access_token if session else ""
    refresh_token = session.refresh_token if session else ""

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserInfo(
            id=user.id,
            email=user.email or payload.email,
            nome=payload.nome,
            role="operador",  # always starts as operador per DB trigger
        ),
    )
