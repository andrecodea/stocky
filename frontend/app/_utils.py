"""Shared utilities: path bootstrap, CSS injection, Supabase helpers."""

import sys
from pathlib import Path

_root    = Path(__file__).resolve().parent.parent.parent
_backend = _root / "backend"

for _p in [str(_root), str(_backend)]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dotenv import load_dotenv
load_dotenv(_root / ".env")

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, .stMetric,
.stDataFrame, .stSelectbox, .stTextInput, .stChatInput {
    font-family: 'Space Grotesk', sans-serif !important;
}

code, pre, .stCode { font-family: 'Space Mono', monospace; font-size: 0.75rem; }
h1 { font-weight: 600 !important; }
h2, h3, h4, h5, h6 { font-weight: 500 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #ede9dc !important;
    border-right: 1px solid #d6d1c4;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: #f5f2ea;
    border-radius: 0.75rem;
    padding: 1rem 1.25rem;
    border: 1px solid #d6d1c4;
}

/* Alert badge */
.alert-badge {
    background: #cb785c;
    color: white;
    border-radius: 0.375rem;
    padding: 0.125rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Button override */
.stButton > button {
    border-radius: 9999px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
}
</style>
"""


def inject_css() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)
