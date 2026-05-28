from fastapi import APIRouter, HTTPException

from services.product_service import (
    listar_produtos,
    buscar_produto,
    criar_produto,
    atualizar_produto,
    deletar_produto,
    listar_estoque_atual,
    Product,
    ProductCreate,
    ProductUpdate,
    ProductWithStock,
)

router = APIRouter()


# GET - listar produtos
@router.get("/produtos", response_model=list[Product])
def get_produtos():
    return listar_produtos()


# GET - buscar produto por ID
@router.get("/produtos/{produto_id}", response_model=Product)
def get_produto(produto_id: str):
    produto = buscar_produto(produto_id)

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


# POST - criar produto
@router.post("/produtos", response_model=Product)
def post_produto(data: ProductCreate):
    return criar_produto(data)


# PUT - atualizar produto
@router.put("/produtos/{produto_id}", response_model=Product)
def put_produto(produto_id: str, data: ProductUpdate):
    produto = atualizar_produto(produto_id, data)

    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


# DELETE - deletar produto
@router.delete("/produtos/{produto_id}")
def delete_produto(produto_id: str):
    deletado = deletar_produto(produto_id)

    if not deletado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return {"success": True}


# GET - listar estoque atual
@router.get("/estoque", response_model=list[ProductWithStock])
def get_estoque():
    return listar_estoque_atual()