"""Authentication request and response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Payload for user login."""

    email: str = Field(..., description="User email address")
    senha: str = Field(..., min_length=6, description="User password")


class SignupRequest(BaseModel):
    """Payload for user registration."""

    email: str = Field(..., description="User email address")
    senha: str = Field(..., min_length=6, description="User password")
    nome: str = Field(..., min_length=1, description="User display name")


class UserInfo(BaseModel):
    """Basic user information returned after auth."""

    id: str
    email: str
    nome: str
    role: str


class AuthResponse(BaseModel):
    """Response after successful login or signup."""

    access_token: str
    refresh_token: str
    user: UserInfo
