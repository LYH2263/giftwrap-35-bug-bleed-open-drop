import pytest

import app.db as dbmod
from app import seed


@pytest.fixture()
def fresh_db(monkeypatch, tmp_path):
    """每个用例独立 sqlite 库，并跑一遍建表/迁移。"""
    monkeypatch.setattr(dbmod, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    yield
