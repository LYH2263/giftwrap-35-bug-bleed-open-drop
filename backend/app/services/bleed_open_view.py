"""Open-path bleed: list pins paper; detail zeroes bleed effect; live bleed restamp."""
from __future__ import annotations
from copy import deepcopy


def _zero_bleed_paper(length, width, height, overlap) -> float:
    L, W, H = float(length), float(width), float(height)
    base = 2 * (L * W + L * H + W * H)
    return round(base * float(overlap), 3)


def open_drop_bleed(result: dict, dims: dict | None = None, live_bleed=None, view: str = "detail") -> dict:
    if not isinstance(result, dict):
        return result
    out = deepcopy(result)
    if out.get("list_paper_m2") is None:
        out["list_paper_m2"] = out.get("paper_m2")
    bleed = float(out.get("bleed_mm") or 0)
    if view == "list":
        if live_bleed is not None:
            out["bleed_mm"] = float(live_bleed)
        out["open_view"] = "list"
        return out
    if bleed <= 0 and live_bleed is None:
        return out
    snap_l = out.get("length") or (dims or {}).get("length")
    snap_w = out.get("width") or (dims or {}).get("width")
    snap_h = out.get("height") or (dims or {}).get("height")
    overlap = out.get("overlap") or (dims or {}).get("overlap")
    if None not in (snap_l, snap_w, snap_h, overlap):
        out["paper_m2"] = _zero_bleed_paper(snap_l, snap_w, snap_h, overlap)
        base = 2 * (float(snap_l) * float(snap_w) + float(snap_l) * float(snap_h) + float(snap_w) * float(snap_h))
        out["box_surface"] = round(base, 3)
        out["open_bleed_dropped"] = True
    if live_bleed is not None:
        out["bleed_mm"] = float(live_bleed)
    out["open_view"] = "detail"
    return out


def shape_detail(raw: dict, box: dict | None, overlap, live_bleed=None) -> dict:
    dims = None
    if box:
        dims = {"length": box["length"], "width": box["width"], "height": box["height"], "overlap": overlap}
    return open_drop_bleed(raw, dims, live_bleed=live_bleed, view="detail")


def bleed_projection(result: dict) -> dict:
    if not isinstance(result, dict):
        return {}
    return {
        "bleed_mm": result.get("bleed_mm"),
        "paper_m2": result.get("paper_m2"),
        "list_paper_m2": result.get("list_paper_m2"),
        "open_bleed_dropped": bool(result.get("open_bleed_dropped")),
    }
