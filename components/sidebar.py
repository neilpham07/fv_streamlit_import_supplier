import streamlit as st
import pandas as pd


def _get_suppliers() -> pd.DataFrame:
    try:
        from database.queries import get_all_suppliers
        return get_all_suppliers()
    except Exception:
        return pd.DataFrame([
            {"supplier_id": "#VND-2024-001", "supplier_name": "Unilever International", "rule_data": "DMS,SKU"},
            {"supplier_id": "#VND-2024-042", "supplier_name": "Procter & Gamble",        "rule_data": "DISTRIBUTOR"},
            {"supplier_id": "#VND-2024-089", "supplier_name": "Nestlé Vietnam",           "rule_data": "DMS,SKU"},
            {"supplier_id": "#VND-2024-112", "supplier_name": "Kao Corporation",          "rule_data": "SKU"},
            {"supplier_id": "#VND-2024-205", "supplier_name": "Suntory PepsiCo",          "rule_data": "DMS,DISTRIBUTOR"},
        ])


@st.dialog("Add New Supplier")
def _add_supplier_dialog():
    with st.form("add_supplier_form"):
        sid    = st.text_input("Supplier ID *", placeholder="#VND-2024-XXX")
        name   = st.text_input("Supplier Name *")
        s_type = st.selectbox("Type", [
            "Tier 1 Manufacturer", "Tier 1 Logistics", "Logistics Partner",
            "Manufacturer", "Distributor", "Bottler/Distributor", "Raw Materials",
        ])
        coop = st.selectbox("Cooperation Form", [
            "Trực tiếp (Direct)", "Ủy thác (Entrusted)",
            "Phân phối (Agency)", "Strategic Partnership",
        ])
        rule     = st.multiselect("Rule Data", ["DMS", "SKU", "DISTRIBUTOR"])
        dms_code = st.text_input("DMS Code", placeholder="DMS-XX-00")
        parent   = st.text_input("Parent Org")
        address  = st.text_area("Address", height=70)

        col_save, col_cancel = st.columns(2)
        if col_save.form_submit_button("Add Supplier", type="primary", use_container_width=True):
            if not sid or not name:
                st.error("Supplier ID and Name are required.")
            else:
                try:
                    from database.queries import insert_supplier
                    import datetime
                    insert_supplier({
                        "supplier_id":    sid.strip(),
                        "supplier_name":  name.strip(),
                        "supplier_type":  s_type,
                        "cooperation_form": coop,
                        "rule_data":      ",".join(rule),
                        "dms_code":       dms_code.strip(),
                        "parent_org":     parent.strip(),
                        "address":        address.strip(),
                        "on_date":        datetime.date.today(),
                        "is_active":      True,
                    })
                    st.success(f"Supplier '{name}' added!")
                    st.session_state.suppliers_cache = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        if col_cancel.form_submit_button("Cancel", use_container_width=True):
            st.rerun()


def render_sidebar():
    with st.sidebar:

        # ── Branding ──────────────────────────────────────────────────────────
        st.markdown("<div style='margin-top:-12px;'>", unsafe_allow_html=True)
        st.image("image/logo finviet.png", width=130)
        st.markdown(
            "</div><hr style='border:none;border-top:1px solid #e9ecef;margin:0 0 10px;'>",
            unsafe_allow_html=True,
        )

        # ── Add Supplier (outlined, neutral) ──────────────────────────────────
        # The `help` param causes Streamlit to set aria-label on the button,
        # which allows precise CSS targeting without :first-of-type hacks.
        if st.button(
            "＋  Add Supplier",
            use_container_width=True,
            key="btn_add",
            help="Add a new supplier to the registry",
        ):
            _add_supplier_dialog()

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # ── Global Search ─────────────────────────────────────────────────────
        search = st.text_input(
            "search",
            placeholder="🔍  Search suppliers...",
            label_visibility="collapsed",
            key="sidebar_search",
        )

        # ── Operations nav ────────────────────────────────────────────────────
        st.markdown('<div class="nav-label">Operations</div>', unsafe_allow_html=True)

        current_page = st.session_state.get("page", "supplier_manage")
        _nav_btn("🗂  Supplier Manage",  "supplier_manage", current_page)

        # ── Brand Folders ─────────────────────────────────────────────────────
        st.markdown('<div class="nav-label">Brand Folders</div>', unsafe_allow_html=True)

        if st.session_state.get("suppliers_cache") is None:
            df = _get_suppliers()
            st.session_state.suppliers_cache = df
        else:
            df = st.session_state.suppliers_cache

        brands = df["supplier_name"].tolist()
        if search:
            brands = [b for b in brands if search.lower() in b.lower()]

        active_brand = st.session_state.get("active_brand", "")

        for brand in brands:
            is_active = brand == active_brand
            # Minimal folder icon — open when active, closed otherwise
            icon = "📂" if is_active else "📁"
            btn_type = "primary" if is_active else "secondary"
            if st.button(
                f"{icon}  {brand}",
                key=f"brand_{brand}",
                type=btn_type,
            ):
                row = df[df["supplier_name"] == brand].iloc[0]
                st.session_state.page               = "brand_sku"
                st.session_state.active_brand       = brand
                st.session_state.active_supplier_id   = row["supplier_id"]
                st.session_state.active_supplier_name = brand
                st.session_state.active_rule_data     = row.get("rule_data", "")
                st.session_state.editing_supplier_id  = None
                st.rerun()

        # ── Footer ────────────────────────────────────────────────────────────
        st.markdown(
            "<hr style='border:none;border-top:1px solid #e9ecef;margin:1.25rem 0 0.5rem;'>",
            unsafe_allow_html=True,
        )
        if st.button("🚪  Log Out", use_container_width=True, key="nav_logout"):
            st.session_state.clear()
            st.rerun()


def _nav_btn(label: str, page_key: str, current_page: str):
    """Render a sidebar nav item — primary (active highlight) vs secondary (text link)."""
    btn_type = "primary" if current_page == page_key else "secondary"
    if st.button(label, key=f"nav_{page_key}", use_container_width=True, type=btn_type):
        st.session_state.page               = page_key
        st.session_state.active_brand       = ""
        st.session_state.editing_supplier_id = None
        st.rerun()
