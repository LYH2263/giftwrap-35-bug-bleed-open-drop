import pytest

from app.engines.wrap_math import BLEED_CALC_ORDER, expand_dims, paper_area, ribbon_estimate

def test_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15)
    assert r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31

def test_ribbon_cross():
    rb = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert rb["ribbon_m"] > 0.5

def test_bleed_zero_keeps_raw_dims():
    r = paper_area(0.30, 0.20, 0.15, 1.15, 0)
    assert (r["eff_length"], r["eff_width"], r["eff_height"]) == (0.30, 0.20, 0.15)
    assert r["bleed_mm"] == 0.0
    assert r["paper_m2"] == 0.31

def test_bleed_expands_both_sides():
    # 出血 50mm：每个维度两侧各出一个出血，有效边长 +0.1m
    assert expand_dims(1.0, 0.5, 0.2, 50) == (1.1, 0.6, 0.3)

def test_bleed_applies_before_overlap():
    # 口径：先扩边得有效几何，再对扩边后表面积乘折边系数
    r = paper_area(1, 1, 1, 1.5, 50)
    assert (r["eff_length"], r["eff_width"], r["eff_height"]) == (1.1, 1.1, 1.1)
    assert r["box_surface"] == 7.26
    assert r["paper_m2"] == 10.89
    assert r["calc_order"] == BLEED_CALC_ORDER == "bleed_then_overlap"

def test_negative_bleed_raises():
    with pytest.raises(ValueError):
        paper_area(1, 1, 1, 1.0, -0.5)
    with pytest.raises(ValueError):
        expand_dims(1, 1, 1, -1)
