from fastapi import APIRouter, Query
from app.schemas.estimate import EstimateRequest
from app.services import estimate_service
router = APIRouter()
@router.get("/estimate")
def get_est(box_id: int = Query(...), overlap: float | None = None, bleed_mm: float | None = None, wrap_style: str = "cross", save: bool = False):
    return estimate_service.run_estimate(box_id, overlap, wrap_style, save, "", bleed_mm)
@router.post("/estimate")
def post_est(body: EstimateRequest):
    return estimate_service.run_estimate(body.box_id, body.overlap, body.wrap_style, body.save, body.note, body.bleed_mm)
