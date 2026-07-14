import streamlit as st

st.set_page_config(
    page_title="SupplyChain Pro | Enterprise MDM",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_css
from components.auth import login_page
from components.sidebar import render_sidebar
from components.supplier_view import render_supplier_view
from components.sku_editor import render_sku_view

inject_css()

# ── One-time DB init ──────────────────────────────────────────────────────────
if "db_ready" not in st.session_state:
    try:
        from database.models import init_db
        init_db()
        st.session_state.db_ready = True
    except Exception:
        st.session_state.db_ready = False   # gracefully degrade to sample data

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_page()
    st.stop()

# ── Authenticated shell ───────────────────────────────────────────────────────
render_sidebar()

page = st.session_state.get("page", "supplier_manage")

with st.spinner("Đang tải..."):
    if page == "supplier_manage":
        render_supplier_view()

    elif page == "brand_sku":
        render_sku_view()

    else:
        st.session_state.page = "supplier_manage"
        st.rerun()
