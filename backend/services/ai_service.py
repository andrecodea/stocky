from agent import build_agent
from services.product_service import ProductWithStock

def _inv_to_txt(inventory: list[ProductWithStock]) -> str:
    lines = []
    for p in inventory:
        status = "⚠️ ABAIXO DO MÍNIMO" if p.abaixo_minimo else "OK"
        lines.append(
            f"- {p.nome} (SKU: {p.sku or 'N/A'}): {p.quantidade_atual} {p.unidade or 'un'}"
            f"(mínimo: {p.estoque_minimo}) [{status}]"
        )
    return "\n".join(lines)

def recommend_restock(inventory: list[ProductWithStock]) -> str:
    agent = build_agent()
    context = (
        f"Estoque atual:\n{_inv_to_txt(inventory)}\n\n"
        "Analise o estoque e recomende quais produtos precisam de reposição, "
        "quanto pedir e por quê."
    )
    result = agent.invoke({"messages": [{"role": "user", "content": context}]})
    return result["messages"][-1].content

def answer_query(query: str, inventory: list[ProductWithStock], history: list) -> str:
    agent = build_agent()
    context = f"Estoque atual:\n{_inv_to_txt(inventory)}\n\n{query}"
    result = agent.invoke({"messages": history + [{"role": "user", "content": context}]})
    return result["messages"][-1].content