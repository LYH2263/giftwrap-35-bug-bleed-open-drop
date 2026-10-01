"""Open-path bleed: list/detail both pin the write-time snapshot.

写入即钉住 —— 开放读取只回放 result_json 中钉死的 bleed_mm / paper_m2 / eff_*，
不读当前盒型尺寸、不读当前默认出血，设置改默认不回刷旧单。
详情（且仅当写入 bleed_mm > 0）另外给出一个基于写入快照的零出血对照面积
zero_bleed_paper_m2，仅供对照，绝不替换主用纸面积 paper_m2。
"""
from __future__ import annotations
from copy import deepcopy

from app.engines.wrap_math import paper_area

_DETAIL = "detail"
_LIST = "list"


def _snapshot_dims(raw: dict):
    """还原写入时（扩出血前）的原始三边(米)与折边系数；信息不足返回 None。"""
    bleed = float(raw.get("bleed_mm") or 0)
    overlap = raw.get("overlap")
    length, width, height = raw.get("length"), raw.get("width"), raw.get("height")
    if None in (length, width, height):
        # 旧行只钉了加边后三边：按 eff = 原边 + 2*bleed/1000 反推
        extra = 2 * bleed / 1000.0
        eff_l, eff_w, eff_h = raw.get("eff_length"), raw.get("eff_width"), raw.get("eff_height")
        if None in (eff_l, eff_w, eff_h):
            return None
        length, width, height = eff_l - extra, eff_w - extra, eff_h - extra
    if None in (length, width, height, overlap):
        return None
    return round(float(length), 6), round(float(width), 6), round(float(height), 6), float(overlap)


def open_run_view(result: dict, view: str = _DETAIL) -> dict:
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if view == _DETAIL:
        bleed = float(out.get("bleed_mm") or 0)
        if bleed > 0:
            dims = _snapshot_dims(out)
            if dims is not None:
                length, width, height, overlap = dims
                if min(length, width, height) > 0:
                    # 统一复用引擎唯一面积口径，仅把出血压到 0 作对照
                    out["zero_bleed_paper_m2"] = paper_area(length, width, height, overlap, 0.0)["paper_m2"]
    out["open_view"] = view
    return out


def bleed_projection(result: dict) -> dict:
    if not isinstance(result, dict):
        return {}
    return {
        "bleed_mm": result.get("bleed_mm"),
        "paper_m2": result.get("paper_m2"),
        "zero_bleed_paper_m2": result.get("zero_bleed_paper_m2"),
    }
