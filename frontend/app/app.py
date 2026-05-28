import sys
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dotenv import load_dotenv
load_dotenv(_root / ".env")

import streamlit as st

st.set_page_config(
    page_title="Stocky",
    page_icon=":material/inventory_2:",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = {
    "": [
        st.Page("pages/1_dashboard.py", title="Dashboard", icon=":material/dashboard:"),
        st.Page("pages/2_estoque.py",   title="Estoque",   icon=":material/inventory_2:"),
        st.Page("pages/3_chat.py",      title="Chat IA",   icon=":material/smart_toy:"),
    ]
}

pg = st.navigation(pages)

# Inicializa estado global uma única vez — persiste entre trocas de página
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lc_history" not in st.session_state:
    st.session_state.lc_history = []
if "recomendacoes" not in st.session_state:
    st.session_state.recomendacoes = None

with st.sidebar:
    st.markdown("### 📦 Stocky")
    st.caption("Gestão inteligente de estoque")
    st.divider()
    st.caption("Powered by Supabase · OpenRouter")

pg.run()
