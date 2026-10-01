from fastapi import APIRouter, HTTPException
from app.repositories import settings_repo
from app.schemas.settings import SettingsUpdate
router = APIRouter()
@router.get("/settings")
def settings(): return settings_repo.get_all()
@router.put("/settings")
def update_settings(body: SettingsUpdate):
    updates = {}
    if body.overlap is not None:
        if body.overlap <= 0:
            raise HTTPException(422, "overlap must be > 0")
        updates["overlap"] = body.overlap
    if body.bleed_mm is not None:
        if body.bleed_mm < 0:
            raise HTTPException(422, "bleed_mm must be >= 0")
        updates["bleed_mm"] = body.bleed_mm
    if updates:
        settings_repo.set_values(updates)
    return settings_repo.get_all()
