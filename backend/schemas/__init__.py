"""Stocky schema re-exports for convenient importing."""

from schemas.auth import AuthResponse, LoginRequest, SignupRequest, UserInfo
from schemas.ai import AiLogCreate, AiLogRead
from schemas.financeiro import FinancialSummary
from schemas.lote import BatchCreate, BatchRead, BatchUpdate
from schemas.movimentacao import (
    MovementCreate,
    MovementRead,
    MovementWithProduct,
    TipoMovimentacao,
)
from schemas.perfil import ProfileAdminUpdate, ProfileRead, ProfileUpdate
from schemas.produto import ProductCreate, ProductRead, ProductUpdate, StockPosition

__all__ = [
    "AuthResponse",
    "AiLogCreate",
    "AiLogRead",
    "BatchCreate",
    "BatchRead",
    "BatchUpdate",
    "FinancialSummary",
    "LoginRequest",
    "MovementCreate",
    "MovementRead",
    "MovementWithProduct",
    "ProductCreate",
    "ProductRead",
    "ProductUpdate",
    "ProfileAdminUpdate",
    "ProfileRead",
    "ProfileUpdate",
    "SignupRequest",
    "StockPosition",
    "TipoMovimentacao",
    "UserInfo",
]
