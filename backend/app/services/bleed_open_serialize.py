from __future__ import annotations
from app.services.bleed_open_view import open_run_view


def open_bleed_for_run(d: dict) -> dict:
    # 开放读取只回放写入快照：不读当前盒型、不读当前默认出血，改设置不回刷旧单。
    raw = d.get("result") or {}
    if isinstance(raw, dict) and raw.get("bleed_mm") is None and d.get("bleed_mm") is not None:
        # 旧行兼容：result_json 缺 bleed_mm 时从列回填
        raw = dict(raw)
        raw["bleed_mm"] = d.get("bleed_mm")
    return open_run_view(raw, view="detail")


def open_bleed_list(raw: dict) -> dict:
    return open_run_view(raw, view="list")
