"""Product endpoints — CRUD on 'produtos' table."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from api.deps import AuthenticatedUser, require_admin, require_any
from schemas.produto import ProductCreate, ProductRead, ProductUpdate
from services import product_service

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("", response_model=list[ProductRead])
async def listar(
    _user: AuthenticatedUser = Depends(require_any),
) -> list[ProductRead]:
    """List all products."""
    return product_service.listar_produtos()


@router.get("/{produto_id}", response_model=ProductRead)
async def buscar(
    produto_id: str,
    _user: AuthenticatedUser = Depends(require_any),
) -> ProductRead:
    """Get a product by ID."""
    return product_service.buscar_produto(produto_id)


@router.post("", response_model=ProductRead, status_code=201)
async def criar(
    payload: ProductCreate,
    _user: AuthenticatedUser = Depends(require_admin),
) -> ProductRead:
    """Create a new product (admin only)."""
    return product_service.criar_produto(payload)


@router.patch("/{produto_id}", response_model=ProductRead)
async def atualizar(
    produto_id: str,
    payload: ProductUpdate,
    _user: AuthenticatedUser = Depends(require_admin),
) -> ProductRead:
    """Partially update a product (admin only)."""
    return product_service.atualizar_produto(produto_id, payload)


@router.delete("/{produto_id}", status_code=204)
async def deletar(
    produto_id: str,
    _user: AuthenticatedUser = Depends(require_admin),
) -> None:
    """Delete a product (admin only)."""
    product_service.deletar_produto(produto_id)
