from pydantic import BaseModel

class EstimateRequest(BaseModel):
    box_id: int
    overlap: float | None = None
    bleed_mm: float | None = None
    wrap_style: str = "cross"
    save: bool = False
    note: str = ""
