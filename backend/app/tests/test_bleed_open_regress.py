from app.services.bleed_open_view import open_run_view


def test_detail_pins_written_area_and_bleed():
    # 带原尺寸快照的写入行：详情主面积/出血必须钉住写入值，不按零出血覆盖
    raw = {
        "bleed_mm": 3.0,
        "paper_m2": 0.4,
        "length": 0.3,
        "width": 0.2,
        "height": 0.1,
        "overlap": 1.15,
    }
    out = open_run_view(raw, view="detail")
    assert out["bleed_mm"] == 3.0
    assert out["paper_m2"] == 0.4
    # 零出血对照独立成字段，且严格小于写入面积
    assert out["zero_bleed_paper_m2"] < raw["paper_m2"]
    assert out["zero_bleed_paper_m2"] == round(2 * (0.3 * 0.2 + 0.3 * 0.1 + 0.2 * 0.1) * 1.15, 3)
    assert out["open_view"] == "detail"


def test_list_pins_without_zero_bleed_field():
    raw = {
        "bleed_mm": 3.0,
        "paper_m2": 0.4,
        "length": 0.3,
        "width": 0.2,
        "height": 0.1,
        "overlap": 1.15,
    }
    out = open_run_view(raw, view="list")
    assert out["bleed_mm"] == 3.0
    assert out["paper_m2"] == 0.4
    assert "zero_bleed_paper_m2" not in out
    assert out["open_view"] == "list"


def test_zero_bleed_run_has_no_comparison_field():
    raw = {
        "bleed_mm": 0.0,
        "paper_m2": 0.31,
        "length": 0.3,
        "width": 0.2,
        "height": 0.15,
        "overlap": 1.15,
    }
    out = open_run_view(raw, view="detail")
    assert out["paper_m2"] == 0.31
    assert "zero_bleed_paper_m2" not in out


def test_legacy_row_with_only_eff_dims_recovers_zero_bleed():
    # 旧行未钉原始三边，仅有加边后三边 + 出血：反推原始边后仍能给对照，主面积不动
    raw = {
        "bleed_mm": 10.0,
        "paper_m2": 0.422,
        "eff_length": 0.32,
        "eff_width": 0.22,
        "eff_height": 0.17,
        "overlap": 1.15,
    }
    out = open_run_view(raw, view="detail")
    assert out["paper_m2"] == 0.422
    assert out["bleed_mm"] == 10.0
    # 反推 0.30/0.20/0.15，零出血面积 = 0.31
    assert out["zero_bleed_paper_m2"] == 0.31
