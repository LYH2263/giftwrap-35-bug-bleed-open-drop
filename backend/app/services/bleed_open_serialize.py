from __future__ import annotations
from app.services.bleed_open_view import pinned_open_view


def open_bleed_for_run(d: dict) -> dict:
    raw = d.get("result") or {}
    if isinstance(raw, dict) and raw.get("bleed_mm") is None and d.get("bleed_mm") is not None:
        # 老数据 result_json 无出血字段：用落库列里写入时的 bleed_mm 钉回，
        # 绝不读取当前设置里的默认出血（设置变基不得回刷旧编号）。
        raw = dict(raw)
        raw["bleed_mm"] = d.get("bleed_mm")
    return pinned_open_view(raw)


def open_bleed_list(raw: dict) -> dict:
    return pinned_open_view(raw)
