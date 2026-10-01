"""Open 视图口径：列表与详情一律回放写入时钉住的 bleed_mm / paper_m2。

仓储 open 路径只做忠实回放 —— 不按零出血重算面积，也不在设置变基后
用当前默认出血回刷旧编号。改造前写入的老数据没有出血字段，等价零出血
口径，统一补 bleed_mm=0 展示。
"""
from __future__ import annotations
from copy import deepcopy


def pinned_open_view(result: dict) -> dict:
    """Return the stored result as written; legacy rows get bleed_mm=0 backfilled."""
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if out.get("bleed_mm") is None:
        out["bleed_mm"] = 0.0
    return out


def bleed_projection(result: dict) -> dict:
    if not isinstance(result, dict):
        return {}
    return {
        "bleed_mm": result.get("bleed_mm"),
        "paper_m2": result.get("paper_m2"),
    }
