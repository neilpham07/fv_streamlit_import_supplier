import streamlit as st


def inject_css():
    st.markdown("""
<style>
/* ── global ── */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 0 !important; }
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

/* ── Sidebar always visible: hide both collapse (<<) and expand (>) buttons ── */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] button {
    display: none !important;
}

/* ── sidebar shell — always visible, block all Streamlit hide mechanisms ── */
section[data-testid="stSidebar"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    transform: translateX(0) !important;
    min-width: 240px !important;
    max-width: 240px !important;
    width: 240px !important;
    background-color: #f8f9fa !important;
    border-right: 1px solid #e9ecef !important;
}
section[data-testid="stSidebar"] > div:first-child { padding: 1rem 0.75rem; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span { color: #495057 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #212529 !important; }

/* ── search input ── */
section[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    border: 1px solid #dee2e6 !important;
    color: #212529 !important;
    border-radius: 8px !important;
    font-size: 0.875rem !important;
}
section[data-testid="stSidebar"] input::placeholder { color: #adb5bd !important; }

/* ── ALL sidebar buttons: clean text-link base ── */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #495057 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    width: 100% !important;
    border-radius: 8px !important;
    padding: 0.45rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    letter-spacing: 0 !important;
    box-shadow: none !important;
    transition: background 0.15s, color 0.15s !important;
}
section[data-testid="stSidebar"] .stButton > button > div,
section[data-testid="stSidebar"] .stButton > button p {
    text-align: left !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #e9ecef !important;
    color: #212529 !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:focus,
section[data-testid="stSidebar"] .stButton > button:active {
    box-shadow: none !important;
    outline: none !important;
}

/* ── "Add Supplier": outlined, neutral – targeted via aria-label (set by help=) ── */
section[data-testid="stSidebar"] button[aria-label="Add a new supplier to the registry"] {
    border: 1.5px dashed #ced4da !important;
    color: #343a40 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] button[aria-label="Add a new supplier to the registry"]:hover {
    border-color: #2563eb !important;
    color: #2563eb !important;
    background: #eff6ff !important;
    border-style: solid !important;
}

/* ── Active nav / brand item: soft blue left-border indicator ── */
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #e8f0fe !important;
    color: #1a56db !important;
    font-weight: 600 !important;
    border-left: 3px solid #2563eb !important;
    border-radius: 0 8px 8px 0 !important;
    padding-left: calc(0.75rem - 1px) !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #dce8fd !important;
    color: #1a56db !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] > div,
section[data-testid="stSidebar"] .stButton > button[kind="primary"] p {
    text-align: left !important;
    width: 100% !important;
}

/* ── nav section labels ── */
.nav-label {
    font-size: 0.67rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #adb5bd;
    padding: 1rem 0.5rem 0.3rem; margin-top: 0;
    text-align: left !important;
}

/* ── left-align ALL text in sidebar ── */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div {
    text-align: left !important;
}

/* ── stat cards ── */
.stat-card {
    background: white; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 1.25rem 1.5rem; display: flex; align-items: center; gap: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.stat-icon {
    width: 52px; height: 52px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center; font-size: 1.5rem; flex-shrink: 0;
}
.stat-value { font-size: 2rem; font-weight: 700; color: #0f172a; line-height: 1; }
.stat-label { font-size: 0.8rem; color: #64748b; font-weight: 500; margin-bottom: 2px; }
.stat-delta { font-size: 0.78rem; color: #16a34a; font-weight: 500; }

/* ── rule-data tag pills ── */
.tag {
    display: inline-block; padding: 2px 7px; border-radius: 4px;
    font-size: 0.7rem; font-weight: 700; margin: 1px 2px;
}
.tag-dms  { background: #dbeafe; color: #1d4ed8; }
.tag-sku  { background: #fef9c3; color: #854d0e; }
.tag-dist { background: #ede9fe; color: #6d28d9; }

/* ── panel header ── */
.panel-badge { font-size: 0.72rem; font-weight: 700; color: #2563eb;
               text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
.panel-title { font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-bottom: 1.25rem; }

/* ── compliance row ── */
.comp-row {
    display: flex; align-items: flex-start; gap: 12px;
    border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;
    background: #fafafa;
}
.comp-title { font-weight: 600; font-size: 0.88rem; color: #1a202c; }
.comp-sub   { font-size: 0.78rem; color: #64748b; }

/* ── login card ── */
.login-card {
    max-width: 440px; margin: 0 auto; padding: 2.5rem 2rem;
    background: white; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.login-logo-wrap {
    text-align: center; margin-bottom: 1.75rem;
}
.login-logo {
    display: inline-flex; background: #1a1f2e; padding: 14px 16px;
    border-radius: 14px; font-size: 2rem; margin-bottom: 12px;
}

/* ── field label ── */
.field-label {
    font-size: 0.72rem; font-weight: 700; color: #374151;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 3px;
}

/* ── table ── */
.tbl-header-cell {
    font-size: 0.76rem; font-weight: 700; color: #6b7280;
    text-transform: uppercase; letter-spacing: 0.04em;
    padding: 10px 6px 6px;
}
.supplier-name-main  { font-weight: 600; font-size: 0.875rem; color: #0f172a; }
.supplier-name-sub   { font-size: 0.74rem; color: #94a3b8; }
.cell-text           { font-size: 0.83rem; color: #374151; }
.status-dot-green    { color: #16a34a; }
.status-dot-red      { color: #dc2626; }

/* ── breadcrumb ── */
.breadcrumb { font-size: 0.82rem; color: #64748b; margin-bottom: 6px; }
.breadcrumb a { color: #2563eb; text-decoration: none; cursor: pointer; }

/* ── autosave bar ── */
.status-bar {
    display: flex; align-items: center; gap: 20px;
    padding: 6px 0; font-size: 0.8rem;
}
.dot-green { color: #16a34a; }
.dot-blue  { color: #2563eb; }
</style>
""", unsafe_allow_html=True)
