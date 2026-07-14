import datetime
import pandas as pd
from sqlalchemy import text
from .connection import engine

# Whitelist prevents SQL injection via column names in dynamic queries
_SUPPLIER_WRITABLE_COLS = {
    "supplier_name", "supplier_type", "cooperation_form", "rule_data",
    "dms_code", "on_date", "off_date", "parent_org", "address", "is_active",
}
_SKU_WRITABLE_COLS = {
    "supplier_id", "supplier_name", "distributor_code", "sku",
    "sku_detail", "is_supplier", "on_date", "off_date", "is_active",
}


def get_all_suppliers() -> pd.DataFrame:
    sql = """
        SELECT supplier_id, supplier_name, supplier_type, cooperation_form,
               rule_data, dms_code, on_date, off_date, parent_org, is_active
        FROM supplier_master
        ORDER BY supplier_id
    """
    return pd.read_sql(sql, engine)


def get_supplier_by_id(supplier_id: str) -> dict:
    sql = text("SELECT * FROM supplier_master WHERE supplier_id = :sid")
    with engine.connect() as conn:
        row = conn.execute(sql, {"sid": supplier_id}).fetchone()
    return dict(row._mapping) if row else {}


def update_supplier(supplier_id: str, fields: dict):
    safe = {k: v for k, v in fields.items() if k in _SUPPLIER_WRITABLE_COLS}
    if not safe:
        return
    set_clause = ", ".join(f"{k} = :{k}" for k in safe)
    sql = text(f"UPDATE supplier_master SET {set_clause}, updated_at = NOW() WHERE supplier_id = :supplier_id")
    with engine.begin() as conn:
        conn.execute(sql, {**safe, "supplier_id": supplier_id})


def insert_supplier(data: dict):
    safe = {k: v for k, v in data.items() if k in _SUPPLIER_WRITABLE_COLS}
    if not safe:
        return
    cols = ", ".join(safe.keys())
    vals = ", ".join(f":{k}" for k in safe)
    sql = text(f"INSERT INTO supplier_master ({cols}) VALUES ({vals})")
    with engine.begin() as conn:
        conn.execute(sql, safe)


def get_sku_by_supplier(supplier_id: str) -> pd.DataFrame:
    sql = text("""
        SELECT supplier_id, supplier_name, distributor_code, sku,
               sku_detail, is_supplier, on_date, off_date, is_active
        FROM supplier_sku_data
        WHERE supplier_id = :sid
        ORDER BY id
    """)
    return pd.read_sql(sql, engine, params={"sid": supplier_id})


def bulk_append_sku(supplier_id: str, supplier_name: str, df: pd.DataFrame):
    df = df.copy()
    df["supplier_id"] = supplier_id
    df["supplier_name"] = supplier_name
    df["created_at"] = datetime.datetime.utcnow()
    df.to_sql(
        "supplier_sku_data", engine,
        if_exists="append", index=False,
        method="multi", chunksize=500,
    )
