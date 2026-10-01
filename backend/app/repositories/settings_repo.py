from app.config import DEFAULT_BLEED_MM, DEFAULT_OVERLAP
from app.db import connect

def get_all():
    c = connect()
    try:
        d = {r["key"]: r["value"] for r in c.execute("SELECT key,value FROM settings").fetchall()}
        d.setdefault("overlap", str(DEFAULT_OVERLAP))
        d.setdefault("bleed_mm", str(DEFAULT_BLEED_MM))
        return d
    finally:
        c.close()

def get_overlap():
    return float(get_all().get("overlap", DEFAULT_OVERLAP))

def get_bleed_mm():
    return float(get_all().get("bleed_mm", DEFAULT_BLEED_MM))

def set_values(values):
    c = connect()
    try:
        c.executemany(
            "INSERT INTO settings(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            [(k, str(v)) for k, v in values.items()],
        )
        c.commit()
    finally:
        c.close()
