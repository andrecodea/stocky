import _utils  # noqa: F401 — path bootstrap + CSS
_utils.inject_css()

import pandas as pd
import streamlit as st

from services.product_service import listar_estoque_atual

st.title("Estoque")
st.caption("Posição atual e recomendações de reposição")

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def _load():
    return listar_estoque_atual()

with st.spinner("Carregando estoque..."):
    estoque = _load()

# ── Tabela de estoque ─────────────────────────────────────────────────────────
st.subheader("Posição atual")

alertas = [p for p in estoque if p.abaixo_minimo]
if alertas:
    names = ", ".join(p.nome for p in alertas[:3])
    suffix = f" +{len(alertas) - 3} mais" if len(alertas) > 3 else ""
    st.warning(f"**{len(alertas)} produto(s) abaixo do mínimo:** {names}{suffix}")

if estoque:
    df = pd.DataFrame([
        {
            "Produto":   p.nome,
            "SKU":       p.sku or "—",
            "Qtd atual": float(p.quantidade_atual),
            "Mínimo":    p.estoque_minimo or 0,
            "Unidade":   p.unidade or "un",
            "Alerta":    "⚠️" if p.abaixo_minimo else "✅",
        }
        for p in estoque
    ])

    st.dataframe(
        df.style.apply(
            lambda row: ["background-color: #fde8e0" if row["Alerta"] == "⚠️" else "" for _ in row],
            axis=1,
        ),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Nenhum produto com movimentação registrada.")

st.divider()

# ── Recomendações IA ──────────────────────────────────────────────────────────
st.subheader("Recomendações")

if "recomendacoes" not in st.session_state:
    st.session_state.recomendacoes = None

if st.button("Analisar estoque", type="primary"):
    if not estoque:
        st.warning("Sem dados de estoque para analisar.")
    else:
        with st.spinner("Analisando com IA..."):
            try:
                from services.ai_service import recommend_restock
                st.session_state.recomendacoes = recommend_restock(estoque)
            except Exception as exc:
                st.session_state.recomendacoes = f"⚠️ Serviço de IA indisponível: {exc}"

if st.session_state.recomendacoes:
    st.markdown(st.session_state.recomendacoes)
else:
    st.caption("Clique em 'Analisar estoque' para gerar recomendações com IA.")
