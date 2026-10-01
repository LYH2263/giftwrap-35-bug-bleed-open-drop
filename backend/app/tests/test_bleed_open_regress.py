from app.services.bleed_open_view import pinned_open_view


def test_detail_keeps_pinned_bleed_and_area():
    # 详情不得再按零出血重算：写入什么就回放什么
    raw = {"bleed_mm": 3.0, "paper_m2": 0.4, "length": 0.3, "width": 0.2, "height": 0.1, "overlap": 1.15}
    out = pinned_open_view(raw)
    assert out["bleed_mm"] == 3.0
    assert out["paper_m2"] == raw["paper_m2"]
    assert "list_paper_m2" not in out
    assert "open_bleed_dropped" not in out


def test_legacy_row_backfills_zero_bleed_only():
    # 改造前老数据无出血字段：补 0 展示，面积原样保留
    out = pinned_open_view({"paper_m2": 0.31})
    assert out["bleed_mm"] == 0.0
    assert out["paper_m2"] == 0.31
