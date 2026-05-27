"""Serviço de produtos do Stocky.

Encapsula acesso à tabela `produtos` e à view `estoque_atual` no Supabase,
expondo schemas Pydantic e operações CRUD utilizadas pela camada de API.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from db.supabase import get_client

_TABLE = "produtos"
_VIEW_ESTOQUE = "estoque_atual"


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


class ProductCreate(BaseModel):
    """Payload para criação de produto.

    Apenas `nome` é obrigatório; os demais campos podem ser preenchidos
    posteriormente (por exemplo, após o enriquecimento via visão computacional).
    """

    nome: str = Field(..., min_length=1)
    sku: str | None = None
    descricao: str | None = None
    preco_custo: Decimal | None = None
    preco_venda: Decimal | None = None
    unidade: str | None = None
    estoque_minimo: int | None = None
    foto_url: str | None = None


class ProductUpdate(BaseModel):
    """Payload de atualização parcial (PATCH).

    Apenas os campos explicitamente enviados são persistidos. A detecção
    é feita via `model_fields_set`, evitando sobrescrever colunas com `None`
    quando o cliente não pretendia limpá-las.
    """

    nome: str | None = Field(default=None, min_length=1)
    sku: str | None = None
    descricao: str | None = None
    preco_custo: Decimal | None = None
    preco_venda: Decimal | None = None
    unidade: str | None = None
    estoque_minimo: int | None = None
    foto_url: str | None = None


class Product(BaseModel):
    """Representação completa de um produto persistido."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    sku: str | None = None
    descricao: str | None = None
    preco_custo: Decimal | None = None
    preco_venda: Decimal | None = None
    unidade: str | None = None
    estoque_minimo: int | None = None
    foto_url: str | None = None
    criado_em: datetime | None = None
    atualizado_em: datetime | None = None


class ProductWithStock(BaseModel):
    """Produto enriquecido com a posição atual de estoque."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nome: str
    sku: str | None = None
    unidade: str | None = None
    estoque_minimo: int | None = None
    quantidade_atual: Decimal
    abaixo_minimo: bool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _serialize_for_supabase(payload: dict) -> dict:
    """Converte tipos Python (Decimal, datetime) para JSON-serializáveis."""
    serialized: dict = {}
    for key, value in payload.items():
        if isinstance(value, Decimal):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized


# ---------------------------------------------------------------------------
# Operações CRUD
# ---------------------------------------------------------------------------


def listar_produtos() -> list[Product]:
    """Retorna todos os produtos cadastrados, ordenados por nome."""
    response = get_client().table(_TABLE).select("*").order("nome").execute()
    return [Product.model_validate(row) for row in response.data or []]


def buscar_produto(produto_id: str) -> Product | None:
    """Busca um produto pelo seu UUID.

    Retorna `None` quando o produto não existe.
    """
    response = (
        get_client().table(_TABLE).select("*").eq("id", produto_id).limit(1).execute()
    )
    rows = response.data or []
    if not rows:
        return None
    return Product.model_validate(rows[0])


def criar_produto(data: ProductCreate) -> Product:
    """Insere um novo produto e retorna o registro persistido."""
    payload = _serialize_for_supabase(data.model_dump(exclude_none=True))
    response = get_client().table(_TABLE).insert(payload).execute()
    return Product.model_validate(response.data[0])


def atualizar_produto(produto_id: str, data: ProductUpdate) -> Product | None:
    """Atualiza parcialmente um produto.

    Apenas os campos presentes em `data.model_fields_set` são enviados ao
    Supabase, permitindo que `None` seja usado para limpar um campo de forma
    explícita quando o cliente assim desejar.

    Retorna `None` quando o produto não existe.
    """
    fields = {name: getattr(data, name) for name in data.model_fields_set}
    if not fields:
        # Nada a atualizar — devolve o estado atual.
        return buscar_produto(produto_id)

    payload = _serialize_for_supabase(fields)
    response = get_client().table(_TABLE).update(payload).eq("id", produto_id).execute()
    rows = response.data or []
    if not rows:
        return None
    return Product.model_validate(rows[0])


def deletar_produto(produto_id: str) -> bool:
    """Remove um produto. Retorna `True` se algo foi deletado."""
    response = get_client().table(_TABLE).delete().eq("id", produto_id).execute()
    return bool(response.data)


def listar_estoque_atual() -> list[ProductWithStock]:
    """Lista a posição atual de estoque via view `estoque_atual`.

    Inclui o flag derivado `abaixo_minimo`, calculado em Python para evitar
    dependência adicional na view.
    """
    response = get_client().table(_VIEW_ESTOQUE).select("*").order("nome").execute()

    resultado: list[ProductWithStock] = []
    for row in response.data or []:
        quantidade_atual = Decimal(str(row.get("quantidade_atual") or 0))
        estoque_minimo = row.get("estoque_minimo")
        abaixo_minimo = estoque_minimo is not None and quantidade_atual < Decimal(
            str(estoque_minimo)
        )
        resultado.append(
            ProductWithStock(
                id=row["produto_id"],
                nome=row["nome"],
                sku=row.get("sku"),
                unidade=row.get("unidade"),
                estoque_minimo=estoque_minimo,
                quantidade_atual=quantidade_atual,
                abaixo_minimo=abaixo_minimo,
            )
        )
    return resultado
