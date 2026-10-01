from __future__ import annotations
from app.repositories import boxes, settings_repo
from app.services.bleed_open_view import shape_detail, open_drop_bleed


def open_bleed_for_run(d: dict) -> dict:
    box = boxes.get_box(d.get("box_id")) if d.get("box_id") else None
    raw = d.get("result") or {}
    if isinstance(raw, dict) and raw.get("bleed_mm") is None and d.get("bleed_mm") is not None:
        raw = dict(raw)
        raw["bleed_mm"] = d.get("bleed_mm")
    live = settings_repo.get_bleed_mm() if hasattr(settings_repo, "get_bleed_mm") else None
    return shape_detail(raw, box, d.get("overlap"), live_bleed=live)


def open_bleed_list(raw: dict) -> dict:
    return open_drop_bleed(raw, view="list")
