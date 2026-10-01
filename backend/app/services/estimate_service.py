from fastapi import HTTPException
from app.engines.wrap_math import paper_area, ribbon_estimate
from app.repositories import boxes, history, settings_repo

def run_estimate(box_id: int, overlap: float | None, wrap_style: str, save: bool, note: str, bleed_mm: float | None = None):
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")
    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()
    bleed = float(bleed_mm) if bleed_mm is not None else settings_repo.get_bleed_mm()
    if bleed < 0:
        raise HTTPException(422, "bleed_mm must be >= 0")
    calc = paper_area(box["length"], box["width"], box["height"], ov, bleed)
    ribbon = ribbon_estimate(box["length"], box["width"], box["height"], wrap_style)
    # 钉入写入时原始三边，供详情零出血对照回放（开放路径不读活盒型）
    payload = {
        **calc,
        "length": box["length"],
        "width": box["width"],
        "height": box["height"],
        "ribbon": ribbon,
        "box_id": box_id,
    }
    run_id = history.insert_run(box_id, ov, payload, note, bleed) if save else None
    return {"box": box, "run_id": run_id, **calc, "ribbon": ribbon}
