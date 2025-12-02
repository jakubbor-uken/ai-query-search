import os
import sys
import logging

import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import logger as logger_module
import ai_search as ai_search_module

def _setup_logging():
    logger_module.Logger()

class FakeApiHandler:
    instances = []

    def __init__(self):
        self.send_calls = []
        FakeApiHandler.instances.append(self)

    class _Msg:
        def __init__(self, content):
            self.content = content

    class _Choice:
        def __init__(self, content):
            self.message = FakeApiHandler._Msg(content)

    class _Response:
        def __init__(self, content):
            self.choices = [FakeApiHandler._Choice(content)]

    def send_request(self, query, db, api_provider, model):
        self.send_calls.append((query, db, api_provider, model))
        return FakeApiHandler._Response(f"response-for-{query}-{model}")

def test_aisearch_initializes_with_api_handler(monkeypatch):
    _setup_logging()

    FakeApiHandler.instances.clear()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    assert isinstance(search.api_handler, FakeApiHandler)
    assert len(FakeApiHandler.instances) == 1

def test_parse_msg_simple_json(monkeypatch):
    _setup_logging()

    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    msg = '{"a": 1, "b": 2}'
    parsed = search.parse_msg(msg)

    assert parsed == {"a": 1, "b": 2}

def test_parse_msg_with_code_fence(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    msg = "```json\n{\"x\": 10, \"y\": 20}\n```"
    parsed = search.parse_msg(msg)

    assert parsed == {"x": 10, "y": 20}

def test_verify_values_valid(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    data = {"a": "0", "b": "42", "c": "100"}
    out = search.verify_values(data)

    assert out is data

def test_verify_values_out_of_bounds_raises(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    with pytest.raises(Exception):
        search.verify_values({"bad": "101"})

def test_verify_values_non_numeric_raises(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    with pytest.raises(ValueError):
        search.verify_values({"bad": "foo"})

def test_get_response_calls_api_handler_and_extracts_content(monkeypatch):
    _setup_logging()

    FakeApiHandler.instances.clear()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    msg = search.get_response("Q", {"k": "v"}, "model-X")

    assert msg == "response-for-Q-model-X"

    assert len(FakeApiHandler.instances) == 1
    fake = FakeApiHandler.instances[0]
    assert fake.send_calls == [
        ("Q", {"k": "v"}, "huggingface", "model-X")
    ]

def test_search_success_first_try(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    calls = {"get_response": 0, "parse": 0, "verify": 0}

    def fake_get_response(query, db, model):
        calls["get_response"] += 1
        assert query == "Q"
        assert db == {"db": True}
        assert model == "M"
        return "raw-msg"

    def fake_parse_msg(msg):
        calls["parse"] += 1
        assert msg == "raw-msg"
        return {"parsed": True}

    def fake_verify_values(msg):
        calls["verify"] += 1
        assert msg == {"parsed": True}
        return {"verified": True}

    monkeypatch.setattr(search, "get_response", fake_get_response)
    monkeypatch.setattr(search, "parse_msg", fake_parse_msg)
    monkeypatch.setattr(search, "verify_values", fake_verify_values)

    times = iter([100.0, 100.123])
    monkeypatch.setattr(ai_search_module, "timer", lambda: next(times))

    result = search.search("Q", {"db": True}, "M")

    assert calls == {"get_response": 1, "parse": 1, "verify": 1}
    assert result["msg"] == {"verified": True}
    assert result["elapsed_time"] == pytest.approx(0.123, rel=0, abs=0.001)

def test_search_retries_on_exception(monkeypatch):
    _setup_logging()
    monkeypatch.setattr(ai_search_module, "ApiHandler", FakeApiHandler)

    search = ai_search_module.AISearch()

    calls = {"get_response": 0, "parse": 0, "verify": 0}

    def fake_get_response(query, db, model):
        calls["get_response"] += 1
        return f"raw-{calls['get_response']}"

    def fake_parse_msg(msg):
        calls["parse"] += 1
        return {"step": calls["parse"], "raw": msg}

    def fake_verify_values(msg):
        calls["verify"] += 1
        if calls["verify"] == 1:
            raise Exception("bad values")
        return {"ok": True, "step": calls["verify"], "raw": msg["raw"]}

    monkeypatch.setattr(search, "get_response", fake_get_response)
    monkeypatch.setattr(search, "parse_msg", fake_parse_msg)
    monkeypatch.setattr(search, "verify_values", fake_verify_values)

    times = iter([10.0, 10.5])
    monkeypatch.setattr(ai_search_module, "timer", lambda: next(times))

    result = search.search("Q", {"db": True}, "M")

    assert calls["get_response"] == 2
    assert calls["parse"] == 2
    assert calls["verify"] == 2

    assert result["msg"]["ok"] is True
    assert result["elapsed_time"] == pytest.approx(0.5, rel=0, abs=0.001)