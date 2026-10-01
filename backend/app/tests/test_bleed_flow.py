import pytest
from fastapi import HTTPException

from app.repositories import history, settings_repo
from app.services import estimate_service

BOOK_BOX_ID = 1  # seed：书型盒 0.30×0.20×0.15，clean


def test_negative_bleed_rejected(fresh_db):
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(BOOK_BOX_ID, None, "cross", False, "", -1)
    assert exc.value.status_code == 422


def test_estimate_uses_default_bleed_from_settings(fresh_db):
    settings_repo.set_values({"bleed_mm": 10})
    r = estimate_service.run_estimate(BOOK_BOX_ID, None, "cross", False, "", None)
    assert r["bleed_mm"] == 10.0
    assert r["eff_length"] == 0.32
    assert r["eff_width"] == 0.22
    assert r["eff_height"] == 0.17


def test_explicit_bleed_overrides_default(fresh_db):
    settings_repo.set_values({"bleed_mm": 10})
    r = estimate_service.run_estimate(BOOK_BOX_ID, None, "cross", False, "", 0)
    assert r["bleed_mm"] == 0.0
    assert (r["eff_length"], r["eff_width"], r["eff_height"]) == (0.30, 0.20, 0.15)


def test_saved_run_pins_bleed_and_area(fresh_db):
    saved = estimate_service.run_estimate(BOOK_BOX_ID, None, "cross", True, "", 5)
    rid = saved["run_id"]
    assert rid is not None
    # 落库须带 bleed_mm、加边后三边、paper_m2
    assert saved["bleed_mm"] == 5.0
    for key in ("eff_length", "eff_width", "eff_height", "paper_m2", "calc_order"):
        assert key in saved

    # 写入后改默认出血：列表与详情两路都必须仍按写入值展示
    settings_repo.set_values({"bleed_mm": 25})
    detail = history.get_run(rid)
    assert detail["bleed_mm"] == 5.0
    assert detail["result"]["bleed_mm"] == 5.0
    assert detail["result"]["paper_m2"] == saved["paper_m2"]
    assert detail["result"]["eff_length"] == saved["eff_length"]
    assert detail["result"]["calc_order"] == "bleed_then_overlap"

    item = next(x for x in history.list_runs() if x["id"] == rid)
    assert item["bleed_mm"] == detail["bleed_mm"] == 5.0
    assert item["result"]["paper_m2"] == detail["result"]["paper_m2"]
    assert item["result"]["bleed_mm"] == detail["result"]["bleed_mm"]

    # 算纸台按写入时出血再干算，须与回看互证
    again = estimate_service.run_estimate(BOOK_BOX_ID, None, "cross", False, "", 5)
    assert again["paper_m2"] == detail["result"]["paper_m2"]
    assert again["eff_length"] == detail["result"]["eff_length"]
    assert again["bleed_mm"] == detail["result"]["bleed_mm"]


def test_settings_reject_negative_bleed(fresh_db):
    from app.routers.settings import update_settings
    from app.schemas.settings import SettingsUpdate

    with pytest.raises(HTTPException) as exc:
        update_settings(SettingsUpdate(bleed_mm=-0.1))
    assert exc.value.status_code == 422
