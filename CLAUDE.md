# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SupplyChain Pro** — an Enterprise Master Data Management (MDM) web application built with Python/Streamlit. The app manages supplier registries, SKU master data, contracts, and compliance tracking for FMCG/distribution companies.

The `image/` directory contains UI design mockups that define the target UX:
- `login.png` — authentication screen
- `home.png` — supplier directory dashboard with stats cards and paginated table
- `supplier.png` — supplier detail/edit slide-over panel
- `sku.png` — per-supplier SKU master data spreadsheet view

## Running the App

```bash
streamlit run app.py
# or for multi-page:
streamlit run Home.py
```

## Intended Architecture

The app follows Streamlit's multi-page app pattern:

```
app.py / Home.py          # entry point, handles login session state
pages/
  supplier_manage.py      # supplier directory + CRUD
  sku_master.py           # per-supplier SKU management
  dashboard.py            # analytics/stats overview
components/
  auth.py                 # login form, session state guard
  sidebar.py              # nav: Dashboard, Supplier Manage; brand folders
  supplier_table.py       # paginated registry table
  supplier_edit_panel.py  # slide-over edit panel (st.sidebar or columns)
  sku_table.py            # spreadsheet-style editable table
data/
  suppliers.py            # supplier CRUD (mock or DB-backed)
  skus.py                 # SKU CRUD
```

## Key Domain Concepts

- **Supplier**: has SupplierID (e.g. `#VND-2024-001`), SupplierName, SupplierType (Tier 1 Manufacturer, Logistics Partner, Distributor, etc.), CooperationForm (Trực tiếp/Direct, Ủy thác/Entrusted, Phân phối/Agency), DMSCode, On/Off Date, ParentOrg, RuleData tags (DMS, SKU, DISTRIBUTOR)
- **SKU**: linked to a supplier, has SupplierID, SupplierName, DistributorCode (e.g. `DIST-LON-04`), SKU code, SKU Detail, and a boolean "Is Supplied" toggle
- **Brand Folders**: Unilever, P&G, Nestlé, Mondelēz — used to filter/group suppliers
- **Supplier tabs**: Directory | Contracts | Compliance
- **Compliance items**: ISO certifications with expiry dates, Financial Audit status

## UI/UX Patterns to Follow

- Dark sidebar (`#1a1f2e`) with white text; active item highlighted in blue
- Stats cards row (Total Suppliers, Active Partners, Pending Review) at top of directory
- Filter tabs (All / Direct / Logistics) above the supplier table
- Export CSV button on all data tables
- Supplier edit opens as a right-side panel (use `st.columns` or `st.sidebar` workaround in Streamlit)
- SKU view is a spreadsheet/data editor (`st.data_editor`) with toggle columns
- Autosave status indicator and "Synchronized with Master DB" badge on SKU page
- Status dots: green for active, red for closed contracts
