import streamlit as st
import pandas as pd


# ── sample fallback ────────────────────────────────────────────────────────────

def _sample_suppliers() -> pd.DataFrame:
    return pd.DataFrame([
        {"supplier_id": "#VND-2024-001", "supplier_name": "Unilever International",
         "supplier_type": "Tier 1 Manufacturer", "cooperation_form": "Trực tiếp (Direct)",
         "rule_data": "DMS,SKU",        "dms_code": "DMS-UL-99",
         "on_date": "2022-01-01", "off_date": None, "parent_org": "Unilever Global PLC", "is_active": True},
        {"supplier_id": "#VND-2024-042", "supplier_name": "Procter & Gamble",
         "supplier_type": "Logistics Partner", "cooperation_form": "Ủy thác (Entrusted)",
         "rule_data": "DISTRIBUTOR",    "dms_code": "DMS-PG-01",
         "on_date": "2021-03-15", "off_date": None, "parent_org": "P&G Indochina", "is_active": True},
        {"supplier_id": "#VND-2024-089", "supplier_name": "Nestlé Vietnam",
         "supplier_type": "Manufacturer", "cooperation_form": "Trực tiếp (Direct)",
         "rule_data": "DMS,SKU",        "dms_code": "DMS-NE-88",
         "on_date": "2020-01-01", "off_date": "2023-12-31", "parent_org": "Nestlé S.A.", "is_active": False},
        {"supplier_id": "#VND-2024-112", "supplier_name": "Kao Corporation",
         "supplier_type": "Distributor", "cooperation_form": "Phân phối (Agency)",
         "rule_data": "SKU",            "dms_code": "DMS-KAO-12",
         "on_date": "2023-10-10", "off_date": None, "parent_org": "Kao Global", "is_active": True},
        {"supplier_id": "#VND-2024-205", "supplier_name": "Suntory PepsiCo",
         "supplier_type": "Bottler/Distributor", "cooperation_form": "Trực tiếp (Direct)",
         "rule_data": "DMS,DISTRIBUTOR","dms_code": "DMS-SP-05",
         "on_date": "2024-01-01", "off_date": None, "parent_org": "SPVB Joint Venture", "is_active": True},
    ])


def _load_suppliers() -> pd.DataFrame:
    try:
        from database.queries import get_all_suppliers
        return get_all_suppliers()
    except Exception:
        return _sample_suppliers()


# ── tag HTML ──────────────────────────────────────────────────────────────────

def _rule_tags(rule_data: str) -> str:
    if not rule_data:
        return ""
    html = []
    for part in str(rule_data).split(","):
        p = part.strip().upper()
        if p == "DMS":
            html.append('<span class="tag tag-dms">DMS</span>')
        elif p == "SKU":
            html.append('<span class="tag tag-sku">SKU</span>')
        elif p in ("DISTRIBUTOR", "PARENT DISTRIBUTOR"):
            html.append('<span class="tag tag-dist">DISTRIBUTOR</span>')
    return "".join(html)


# ── main view ─────────────────────────────────────────────────────────────────

def render_supplier_view():
    # Header
    st.markdown('<h2 style="margin:0 0 4px;color:#0f172a;font-weight:700;">Supplier Master Data</h2>', unsafe_allow_html=True)

    df_all = _load_suppliers()

    # ── Stats ──
    total   = len(df_all)
    active  = int(df_all["is_active"].sum()) if "is_active" in df_all.columns else total
    pending = total - active

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#dbeafe;">👥</div>
        <div>
            <div class="stat-label">Total Suppliers</div>
            <div class="stat-value">{total:,}</div>
            <div class="stat-delta">↑ +12% from last month</div>
        </div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#dcfce7;">✅</div>
        <div>
            <div class="stat-label">Active Partners</div>
            <div class="stat-value">{active:,}</div>
        </div>
    </div>""", unsafe_allow_html=True)
    c3.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:#fef3c7;">⏳</div>
        <div>
            <div class="stat-label">Pending Review</div>
            <div class="stat-value">{pending}</div>
            <div class="stat-delta" style="color:#92400e;">Audit required for {pending} vendors</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:1rem 0 0.5rem;'></div>", unsafe_allow_html=True)

    # ── Filter bar ──
    col_filter, col_export = st.columns([4, 1])
    with col_filter:
        f_opt = st.radio("", ["All", "Direct", "Logistics"], horizontal=True, key="dir_filter", label_visibility="collapsed")
    with col_export:
        st.download_button(
            "⬇ Export CSV",
            df_all.to_csv(index=False).encode(),
            "suppliers.csv", "text/csv",
            use_container_width=True,
        )

    # Apply filter
    df = df_all.copy()
    if f_opt == "Direct":
        df = df[df["cooperation_form"].str.contains("Direct|Trực tiếp", case=False, na=False)]
    elif f_opt == "Logistics":
        df = df[df["supplier_type"].str.contains("Logistics", case=False, na=False)]

    # ── Layout: table only or table + edit panel ──
    editing_id = st.session_state.get("editing_supplier_id")

    if editing_id:
        col_tbl, col_panel = st.columns([3, 2], gap="medium")
        with col_tbl:
            _render_table(df)
        with col_panel:
            _render_edit_panel(editing_id)
    else:
        _render_table(df)


# ── table ─────────────────────────────────────────────────────────────────────

def _render_table(df: pd.DataFrame):
    COLS    = [1.4, 2.2, 1.8, 1.7, 1.6, 1.0, 1.4, 1.8]
    HEADERS = ["Supplier ID", "Supplier Name", "Type", "Cooperation", "Rule Data", "DMS", "On Date", "Parent Org"]

    # Header row
    header_cols = st.columns(COLS)
    for col, h in zip(header_cols, HEADERS):
        col.markdown(f'<div class="tbl-header-cell">{h}</div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin:0 0 4px;border-color:#f0f0f0;'>", unsafe_allow_html=True)

    for _, row in df.iterrows():
        sid       = str(row.get("supplier_id", ""))
        is_active = bool(row.get("is_active", True))
        on_date   = str(row.get("on_date", "") or "")[:10]
        off_date  = str(row.get("off_date", "") or "")[:10]
        dot_color = "#16a34a" if is_active else "#dc2626"
        status    = "Present" if is_active else f"Closed {off_date}"

        cells = st.columns(COLS)

        # Supplier ID as clickable button
        if cells[0].button(sid, key=f"sel_{sid}", help="Click to open edit panel"):
            if st.session_state.get("editing_supplier_id") == sid:
                st.session_state.editing_supplier_id = None
            else:
                st.session_state.editing_supplier_id = sid
            st.rerun()

        cells[1].markdown(f"""
        <div>
            <div class="supplier-name-main">{row.get('supplier_name','')}</div>
            <div class="supplier-name-sub">{str(row.get('supplier_type',''))[:28]}</div>
        </div>""", unsafe_allow_html=True)

        cells[2].markdown(f'<div class="cell-text">{row.get("supplier_type","")}</div>', unsafe_allow_html=True)
        cells[3].markdown(f'<div class="cell-text">{row.get("cooperation_form","")}</div>', unsafe_allow_html=True)
        cells[4].markdown(_rule_tags(row.get("rule_data", "")), unsafe_allow_html=True)
        cells[5].markdown(f'<div class="cell-text">{row.get("dms_code","")}</div>', unsafe_allow_html=True)
        cells[6].markdown(f"""
        <div class="cell-text">
            <span style="color:{dot_color};">●</span> {on_date}<br>
            <small style="color:{dot_color};">{status}</small>
        </div>""", unsafe_allow_html=True)
        cells[7].markdown(f'<div class="cell-text">{row.get("parent_org","")}</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#f0f0f0;'>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.8rem;color:#64748b;padding:4px 0;">Showing 1 to {len(df)} of {len(df)} suppliers</div>', unsafe_allow_html=True)


# ── edit panel ────────────────────────────────────────────────────────────────

_TYPE_OPTIONS = [
    "Tier 1 Manufacturer", "Tier 1 Logistics", "Logistics Partner",
    "Manufacturer", "Distributor", "Bottler/Distributor", "Raw Materials",
]
_COOP_OPTIONS = [
    "Trực tiếp (Direct)", "Ủy thác (Entrusted)",
    "Phân phối (Agency)", "Strategic Partnership",
]


def _render_edit_panel(supplier_id: str):
    # Try DB first, fall back to session cache, then sample data
    supplier = {}
    update_fn = None
    try:
        from database.queries import get_supplier_by_id, update_supplier as _upd
        supplier = get_supplier_by_id(supplier_id) or {}
        update_fn = _upd
    except Exception:
        pass

    if not supplier:
        cache = st.session_state.get("suppliers_cache")
        if cache is not None and not cache.empty:
            rows = cache[cache["supplier_id"] == supplier_id]
            if not rows.empty:
                supplier = rows.iloc[0].to_dict()

    if not supplier:
        supplier = next(
            (r for r in _sample_suppliers().to_dict("records") if r["supplier_id"] == supplier_id),
            {"supplier_id": supplier_id, "supplier_name": supplier_id},
        )

    st.markdown('<div class="panel-badge">Editing Entry</div>', unsafe_allow_html=True)

    col_title, col_close = st.columns([5, 1])
    col_title.markdown(
        f'<div class="panel-title">Edit Supplier:<br>{supplier.get("supplier_name","")}</div>',
        unsafe_allow_html=True,
    )
    if col_close.button("✕", key="close_panel", help="Close panel"):
        st.session_state.editing_supplier_id = None
        st.rerun()

    cur_type = supplier.get("supplier_type", "")
    cur_coop = supplier.get("cooperation_form", "")
    type_idx = _TYPE_OPTIONS.index(cur_type) if cur_type in _TYPE_OPTIONS else 0
    coop_idx = _COOP_OPTIONS.index(cur_coop) if cur_coop in _COOP_OPTIONS else 0

    with st.form(f"edit_form_{supplier_id}"):
        st.markdown(
            'Supplier Name &nbsp;<span style="color:#dc2626;font-size:0.72rem;font-weight:700;">REQUIRED</span>',
            unsafe_allow_html=True,
        )
        name = st.text_input("name", value=supplier.get("supplier_name", ""), label_visibility="collapsed")

        col_t, col_d = st.columns(2)
        with col_t:
            st.markdown("**Type**")
            s_type = st.selectbox("type", _TYPE_OPTIONS, index=type_idx, label_visibility="collapsed")
        with col_d:
            st.markdown("**DMS Code**")
            dms = st.text_input("dms", value=supplier.get("dms_code", ""), label_visibility="collapsed")

        st.markdown("**Cooperation Form**")
        coop = st.selectbox("coop", _COOP_OPTIONS, index=coop_idx, label_visibility="collapsed")

        st.markdown("**Address Details**")
        address = st.text_area("addr", value=supplier.get("address", ""), height=72, label_visibility="collapsed")

        col_save, col_cancel = st.columns(2)
        saved     = col_save.form_submit_button("Save Changes", type="primary", use_container_width=True)
        cancelled = col_cancel.form_submit_button("Cancel", use_container_width=True)

    if saved:
        updates = {
            "supplier_name":    name,
            "supplier_type":    s_type,
            "dms_code":         dms,
            "cooperation_form": coop,
            "address":          address,
        }
        # Persist to DB if available
        if update_fn:
            try:
                update_fn(supplier_id, updates)
            except Exception as e:
                st.warning(f"DB unavailable — changes saved locally only. ({e})")
        # Always update session cache so the table reflects the change immediately
        cache = st.session_state.get("suppliers_cache")
        if cache is not None and not cache.empty:
            for k, v in updates.items():
                if k in cache.columns:
                    cache.loc[cache["supplier_id"] == supplier_id, k] = v
            st.session_state.suppliers_cache = cache
        else:
            st.session_state.suppliers_cache = None
        st.success("Saved successfully!")
        st.session_state.editing_supplier_id = None
        st.rerun()

    if cancelled:
        st.session_state.editing_supplier_id = None
        st.rerun()
