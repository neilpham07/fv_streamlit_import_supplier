from sqlalchemy import text
from .connection import engine

_DDL = [
    """
    CREATE TABLE IF NOT EXISTS supplier_master (
        supplier_id      VARCHAR(50)  PRIMARY KEY,
        supplier_name    VARCHAR(255) NOT NULL,
        supplier_type    VARCHAR(100),
        cooperation_form VARCHAR(100),
        rule_data        VARCHAR(200),
        dms_code         VARCHAR(50),
        on_date          DATE,
        off_date         DATE,
        parent_org       VARCHAR(255),
        address          TEXT,
        is_active        BOOLEAN DEFAULT TRUE,
        created_at       TIMESTAMP DEFAULT NOW(),
        updated_at       TIMESTAMP DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS supplier_sku_data (
        id               SERIAL PRIMARY KEY,
        supplier_id      VARCHAR(50),
        supplier_name    VARCHAR(255),
        distributor_code VARCHAR(100),
        sku              VARCHAR(100),
        sku_detail       TEXT,
        is_supplier      BOOLEAN DEFAULT TRUE,
        on_date          DATE,
        off_date         DATE,
        is_active        BOOLEAN DEFAULT TRUE,
        created_at       TIMESTAMP DEFAULT NOW()
    );
    """,
    """
    INSERT INTO supplier_master
        (supplier_id, supplier_name, supplier_type, cooperation_form,
         rule_data, dms_code, on_date, parent_org, is_active)
    VALUES
        ('#VND-2024-001','Unilever International','Tier 1 Manufacturer','Trực tiếp (Direct)','DMS,SKU','DMS-UL-99','2022-01-01','Unilever Global PLC',TRUE),
        ('#VND-2024-042','Procter & Gamble','Logistics Partner','Ủy thác (Entrusted)','DISTRIBUTOR','DMS-PG-01','2021-03-15','P&G Indochina',TRUE),
        ('#VND-2024-089','Nestlé Vietnam','Manufacturer','Trực tiếp (Direct)','DMS,SKU','DMS-NE-88','2020-01-01','Nestlé S.A.',FALSE),
        ('#VND-2024-112','Kao Corporation','Distributor','Phân phối (Agency)','SKU','DMS-KAO-12','2023-10-10','Kao Global',TRUE),
        ('#VND-2024-205','Suntory PepsiCo','Bottler/Distributor','Trực tiếp (Direct)','DMS,DISTRIBUTOR','DMS-SP-05','2024-01-01','SPVB Joint Venture',TRUE)
    ON CONFLICT (supplier_id) DO NOTHING;
    """,
]


def init_db():
    with engine.begin() as conn:
        for stmt in _DDL:
            conn.execute(text(stmt))
