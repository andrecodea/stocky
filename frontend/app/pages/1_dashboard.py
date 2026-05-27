import _utils  # noqa: F401 — path bootstrap + CSS
_utils.inject_css()

import pandas as pd
import streamlit as st

from backend.services.product_service import listar_produtos, listar_estoque_atual
from backend.db.supabase import get_client

st.title("Dashboard")
st.caption("Visão geral do catálogo e movimentações")

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def _load():
    produtos = listar_produtos()
    estoque  = listar_estoque_atual()
    movs_raw = (
        get_client()
        .table("movimentacoes")
        .select("*, produtos(nome)")
        .order("criado_em", desc=True)
        .limit(20)
        .execute()
        .data or []
    )
    return produtos, estoque, movs_raw

with st.spinner("Carregando..."):
    produtos, estoque, movs_raw = _load()

alertas = sum(1 for p in estoque if p.abaixo_minimo)

# ── KPIs ─────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
c1.metric("Produtos cadastrados", len(produtos))
c2.metric("Alertas de estoque",   alertas,  delta=f"-{alertas} abaixo do mínimo" if alertas else None,
          delta_color="inverse")
c3.metric("Movimentações (recentes)", len(movs_raw))

st.divider()

# ── Produtos table ────────────────────────────────────────────────────────────
st.subheader("Produtos")

if produtos:
    df = pd.DataFrame([
        {
            "Nome":           p.nome,
            "SKU":            p.sku or "—",
            "Custo (R$)":     float(p.preco_custo or 0),
            "Venda (R$)":     float(p.preco_venda or 0),
            "Unidade":        p.unidade or "—",
            "Estoque mínimo": p.estoque_minimo or 0,
        }
        for p in produtos
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum produto cadastrado.")

st.divider()

# ── Movimentações recentes ────────────────────────────────────────────────────
st.subheader("Movimentações recentes")

if movs_raw:
    TIPO_LABEL = {"entrada": "🟢 Entrada", "saida": "🔴 Saída", "ajuste": "🟡 Ajuste"}
    df_mov = pd.DataFrame([
        {
            "Data":      m["criado_em"][:19].replace("T", " "),
            "Produto":   (m.get("produtos") or {}).get("nome", m["produto_id"][:8]),
            "Tipo":      TIPO_LABEL.get(m["tipo"], m["tipo"]),
            "Qtd":       m["quantidade"],
            "Observação": m.get("observacao") or "—",
        }
        for m in movs_raw
    ])
    st.dataframe(df_mov, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma movimentação registrada.")
