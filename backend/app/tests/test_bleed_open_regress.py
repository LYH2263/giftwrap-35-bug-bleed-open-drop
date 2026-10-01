from app.services.bleed_open_view import open_drop_bleed

def test_detail_ignores_bleed_mm():
    raw = {"bleed_mm": 3.0, "paper_m2": 0.4, "length": 0.3, "width": 0.2, "height": 0.1, "overlap": 1.15}
    out = open_drop_bleed(raw, view="detail")
    assert out["bleed_mm"] == 3.0
    assert out["paper_m2"] < raw["paper_m2"]
    assert out.get("list_paper_m2") == 0.4
