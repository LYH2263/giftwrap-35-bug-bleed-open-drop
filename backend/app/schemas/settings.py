from pydantic import BaseModel

class SettingsUpdate(BaseModel):
    overlap: float | None = None
    bleed_mm: float | None = None
