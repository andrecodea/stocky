import _utils  # noqa: F401 — path bootstrap + CSS
_utils.inject_css()

import streamlit as st

from services.product_service import listar_estoque_atual

st.title("Chat IA")
st.caption("Tire dúvidas sobre o estoque com o agente inteligente")

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # list[dict] role/content

if "lc_history" not in st.session_state:
    st.session_state.lc_history = []     # list[dict] passed to answer_query

# ── Sidebar controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.divider()
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.lc_history   = []
        st.rerun()

# ── Render history ────────────────────────────────────────────────────────────
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Pergunte sobre o estoque, reposições, movimentações..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.session_state.lc_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    estoque = listar_estoque_atual()

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                from services.ai_service import answer_query
                response = answer_query(
                    query=prompt,
                    inventory=estoque,
                    history=st.session_state.lc_history[:-1],
                )
            except Exception as exc:
                response = f"⚠️ Serviço de IA indisponível: {exc}"

        st.markdown(response)

    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.session_state.lc_history.append({"role": "assistant", "content": response})
