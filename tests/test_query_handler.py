import os
import sys
import json
import logging

import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import logger as logger_module
import query_handler as qh_module

class FakeAISearch:
    instances = []

    def __init__(self):
        self.search_calls = []
        FakeAISearch.instances.append(self)

    def search(self, query, db, model):
        self.search_calls.append((query, db, model))
        return {"msg": f"ans-{query}-{model}", "elapsed_time": 0.123}


def _setup_logging():
    logger_module.Logger()

def test_queryhandler_initializes_with_aisearch(monkeypatch):
    _setup_logging()

    FakeAISearch.instances.clear()
    monkeypatch.setattr(qh_module, "AISearch", FakeAISearch)

    handler = qh_module.QueryHandler()

    assert isinstance(handler.ai_search, FakeAISearch)
    assert handler.db is None
    assert len(FakeAISearch.instances) == 1

def test_load_database_success(tmp_path, monkeypatch):
    _setup_logging()
    monkeypatch.setattr(qh_module, "AISearch", FakeAISearch)

    data = {"foo": 1, "bar": ["x", "y"]}
    db_path = tmp_path / "db.json"
    db_path.write_text(json.dumps(data), encoding="utf-8")

    handler = qh_module.QueryHandler()
    handler.load_database(str(db_path))

    assert handler.db == data


def test_load_database_file_not_found(monkeypatch, caplog):
    _setup_logging()
    monkeypatch.setattr(qh_module, "AISearch", FakeAISearch)

    handler = qh_module.QueryHandler()

    missing_path = "/path/that/does/not/exist.json"

    with caplog.at_level(logging.ERROR, logger="query_handler"):
        handler.load_database(missing_path)

    assert handler.db is None

    msgs = [r.getMessage() for r in caplog.records]
    assert any("File not found" in m for m in msgs)

def test_load_database_invalid_json(tmp_path, monkeypatch, caplog):
    _setup_logging()
    monkeypatch.setattr(qh_module, "AISearch", FakeAISearch)

    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{ not-valid-json", encoding="utf-8")

    handler = qh_module.QueryHandler()

    with caplog.at_level(logging.ERROR, logger="query_handler"):
        handler.load_database(str(bad_path))

    assert handler.db is None

    msgs = [r.getMessage() for r in caplog.records]
    assert any("Invalid JSON" in m for m in msgs)

def test_send_query_raises_if_db_is_none(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(qh_module, "AISearch", FakeAISearch)

    handler = qh_module.QueryHandler()

    with pytest.raises(ValueError) as excinfo:
        handler.send_query("some query", "some-model")

    assert "Database was not read correctly" in str(excinfo.value)

def test_send_query_calls_aisearch_with_correct_args(monkeypatch):
    _setup_logging()

    FakeAISearch.instances.clear()
    monkeypatch.setattr(qh_module, "AISearch", FakeAISearch)

    handler = qh_module.QueryHandler()
    fake_db = {"k": "v"}
    handler.db = fake_db

    result = handler.send_query("Q", "M")

    assert result == {"msg": "ans-Q-M", "elapsed_time": 0.123}

    assert len(FakeAISearch.instances) == 1
    fake = FakeAISearch.instances[0]
    assert fake.search_calls == [("Q", fake_db, "M")]