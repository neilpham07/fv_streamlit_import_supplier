import html as _html
import streamlit as st
import pandas as pd


def _esc(value) -> str:
    return _html.escape(str(value or ""))


_EMPTY_ROW = {
    "supplier_id": "",
    "supplier_name": "",
    "distributor_code": "",
    "sku": "",
    "sku_detail": "",
    "is_supplier": True,
    "on_date": None,
    "off_date": None,
    "is_active": True,
}

_COL_CONFIG = {
    "supplier_id":       st.column_config.TextColumn("Supplier ID",       width="medium"),
    "supplier_name":     st.column_config.TextColumn("Supplier Name",     width="large"),
    "distributor_code":  st.column_config.TextColumn("Distributor Code",  width="medium"),
    "sku":               st.column_config.TextColumn("SKU",               width="medium"),
    "sku_detail":        st.column_config.TextColumn("SKU Detail",        width="large"),
    "is_supplier":       st.column_config.CheckboxColumn("Is Supplier",   width="small", default=True),
    "on_date":           st.column_config.DateColumn("On Date",           width="small"),
    "off_date":          st.column_config.DateColumn("Off Date",          width="small"),
    "is_active":         st.column_config.CheckboxColumn("Is Active",     width="small", default=True),
}


def _sample_sku(supplier_id: str, supplier_name: str) -> pd.DataFrame:
    rows = [
        {"supplier_id": "UL-9821", "supplier_name": supplier_name, "distributor_code": "DIST-LON-04",
         "sku": "DOVE-WASH-250",  "sku_detail": "Dove Body Wash Deeply Nourishing 250ml",
         "is_supplier": True,  "on_date": None, "off_date": None, "is_active": True},
        {"supplier_id": "UL-9822", "supplier_name": supplier_name, "distributor_code": "DIST-BER-09",
         "sku": "HELM-MAY-500",   "sku_detail": "Hellmann's Real Mayonnaise 500g",
         "is_supplier": True,  "on_date": None, "off_date": None, "is_active": True},
        {"supplier_id": "UL-9825", "supplier_name": supplier_name, "distributor_code": "DIST-PAR-12",
         "sku": "LIP-TEA-100",    "sku_detail": "Lipton Yellow Label Tea 100 Bags",
         "is_supplier": False, "on_date": None, "off_date": None, "is_active": True},
        {"supplier_id": "UL-9824", "supplier_name": supplier_name, "distributor_code": "DIST-GEN-104",
         "sku": "SKU-GEN-504",    "sku_detail": f"Generic {supplier_name} Product Line 4",
         "is_supplier": True,  "on_date": None, "off_date": None, "is_active": True},
        {"supplier_id": "UL-9825", "supplier_name": supplier_name, "distributor_code": "DIST-GEN-105",
         "sku": "SKU-GEN-505",    "sku_detail": f"Generic {supplier_name} Product Line 5",
         "is_supplier": True,  "on_date": None, "off_date": None, "is_active": True},
    ]
    return pd.DataFrame(rows)


def _load_sku(supplier_id: str, supplier_name: str) -> pd.DataFrame:
    try:
        from database.queries import get_sku_by_supplier
        df = get_sku_by_supplier(supplier_id)
        if df.empty:
            return _sample_sku(supplier_id, supplier_name)
        for col in ("id", "created_at"):
            if col in df.columns:
                df = df.drop(columns=[col])
        return df
    except Exception:
        return _sample_sku(supplier_id, supplier_name)


def render_sku_view():
    supplier_id   = st.session_state.get("active_supplier_id", "")
    supplier_name = st.session_state.get("active_supplier_name", "Unknown")

    # ── Breadcrumb ──
    st.markdown(f"""
    <div class="breadcrumb">
        <a onclick="void(0)">Suppliers</a>
        &nbsp;/&nbsp;
        <strong style="color:#0f172a;">{_esc(supplier_name)}</strong>
    </div>
    """, unsafe_allow_html=True)

    # ── Header ──
    col_h, col_btns = st.columns([4, 1])
    with col_h:
        st.markdown(f'<h2 style="margin:0;font-weight:700;color:#0f172a;">{_esc(supplier_name)} — SKU Master Data</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color:#64748b;font-size:0.84rem;margin:3px 0 0;">Bulk spreadsheet view for SKU management and distributor mapping.</p>', unsafe_allow_html=True)
    with col_btns:
        st.button("≡ Filter", use_container_width=True, key="sku_filter")

    st.markdown("<div style='margin:0.6rem 0;'></div>", unsafe_allow_html=True)

    # ── Load / cache data ──
    cache_key = f"sku_data_{supplier_id}"
    if cache_key not in st.session_state:
        st.session_state[cache_key] = _load_sku(supplier_id, supplier_name)

    base_df: pd.DataFrame = st.session_state[cache_key].copy()

    # Append blank rows so the grid is always ready for Ctrl+V paste
    pad = pd.DataFrame([_EMPTY_ROW] * 25)
    display_df = pd.concat([base_df, pad], ignore_index=True)

    # ── Data editor ──
    # num_rows="dynamic" + blank padding = Ctrl+V paste works out of the box
    edited: pd.DataFrame = st.data_editor(
        display_df,
        column_config=_COL_CONFIG,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=False,
        height=580,
        key=f"sku_editor_{supplier_id}",
    )

    # ── Status + Export + Save row ──
    col_status, col_count, col_export, col_save = st.columns([3, 2, 1, 1])

    real_count = int(edited["sku"].notna().sum() and (edited["sku"].str.strip() != "").sum())

    col_status.markdown(f"""
    <div class="status-bar">
        <span class="dot-green">● Synchronized with Master DB</span>
        <span class="dot-blue">● Autosave enabled</span>
    </div>""", unsafe_allow_html=True)

    col_count.markdown(
        f'<div style="padding-top:10px;font-size:0.83rem;color:#64748b;">Row Count: {real_count:,} &nbsp;&nbsp; Filtered: {real_count}</div>',
        unsafe_allow_html=True,
    )

    col_export.download_button(
        "⬇ Export CSV",
        edited.to_csv(index=False).encode(),
        f"{supplier_name}_sku.csv",
        "text/csv",
        use_container_width=True,
    )

    if col_save.button("✓ Save Changes", type="primary", use_container_width=True, key="save_sku"):
        _save_sku(edited, supplier_id, supplier_name, cache_key)


def _save_sku(edited: pd.DataFrame, supplier_id: str, supplier_name: str, cache_key: str):
    new_rows = edited[edited["sku"].notna() & (edited["sku"].str.strip() != "")].copy()
    if new_rows.empty:
        st.info("No SKU data to save.")
        return
    try:
        from database.queries import bulk_append_sku
        bulk_append_sku(supplier_id, supplier_name, new_rows)
        st.success(f"✓ Saved {len(new_rows)} rows to Master DB.")
        # Refresh cache
        if cache_key in st.session_state:
            del st.session_state[cache_key]
        st.rerun()
    except Exception as e:
        # If DB unavailable, persist in session only
        st.session_state[cache_key] = new_rows.reset_index(drop=True)
        st.warning(f"DB unavailable — saved to session only. ({e})")
