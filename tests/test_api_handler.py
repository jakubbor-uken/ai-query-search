import os
import sys
import json
import logging

import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import logger as logger_module
import api_handler as api_handler_module

def _setup_logging():
    logger_module.Logger()

class FakeOpenAI:
    instances = []

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.last_create_args = None

        class _Completions:
            def __init__(self, outer):
                self._outer = outer

            def create(self, model, messages):
                self._outer.last_create_args = {
                    "model": model,
                    "messages": messages,
                }
                return {
                    "model": model,
                    "messages": messages,
                    "stub": True,
                }

        class _Chat:
            def __init__(self, outer):
                self.completions = _Completions(outer)

        self.chat = _Chat(self)
        FakeOpenAI.instances.append(self)

def test_apihandler_init_sets_prompt_and_logs():
    _setup_logging()
    handler = api_handler_module.ApiHandler()

    assert isinstance(handler.ai_prompt_assist, str)
    assert handler.ai_prompt_assist.strip() != ""

def test_send_request_routes_to_huggingface(monkeypatch):
    _setup_logging()

    calls = {}

    def fake_hf_request(self, query, db, model):
        calls["args"] = (query, db, model)
        return {"ok": True}

    monkeypatch.setattr(api_handler_module.ApiHandler, "huggingface_request", fake_hf_request)

    handler = api_handler_module.ApiHandler()
    result = handler.send_request("Q1", {"db": True}, "huggingface", "model-X")

    assert result == {"ok": True}
    assert calls["args"] == ("Q1", {"db": True}, "model-X")


def test_send_request_invalid_provider_raises():
    _setup_logging()
    handler = api_handler_module.ApiHandler()

    with pytest.raises(ValueError) as excinfo:
        handler.send_request("Q", {"db": True}, "openai", "model-X")

    assert "Wrong API provider specified" in str(excinfo.value)

def test_huggingface_request_builds_client_and_calls_create(tmp_path, monkeypatch, caplog):
    _setup_logging()

    keys = [
        {"id": "huggingface2", "key": "hf-secret-key"},
        {"id": "other", "key": "zzz"},
    ]
    keys_path = tmp_path / "keys.json"
    keys_path.write_text(json.dumps(keys), encoding="utf-8")

    monkeypatch.setenv("AI_API_KEYS", str(keys_path))

    FakeOpenAI.instances.clear()
    monkeypatch.setattr(api_handler_module, "OpenAI", FakeOpenAI)

    handler = api_handler_module.ApiHandler()

    query = "test query"
    db = {"x": 1}
    model = "deepseek/whatever"

    with caplog.at_level(logging.INFO, logger="api_handler"):
        completion = handler.huggingface_request(query, db, model)

    assert len(FakeOpenAI.instances) == 1
    client = FakeOpenAI.instances[0]

    assert client.base_url == "https://router.huggingface.co/v1"
    assert client.api_key == "hf-secret-key"

    assert client.last_create_args is not None
    assert client.last_create_args["model"] == model

    messages = client.last_create_args["messages"]
    assert isinstance(messages, list)
    assert messages[0]["role"] == "user"

    expected_content = f"{query}" + handler.ai_prompt_assist + str(db)
    assert messages[0]["content"] == expected_content

    assert completion["stub"] is True

    msgs = [r.getMessage() for r in caplog.records]
    assert any("Sending request to HuggingFace API" in m for m in msgs)
    assert any("Response received" in m for m in msgs)

def test_huggingface_request_raises_if_key_missing(tmp_path, monkeypatch):
    _setup_logging()

    keys = [
        {"id": "something_else", "key": "nope"},
    ]
    keys_path = tmp_path / "keys.json"
    keys_path.write_text(json.dumps(keys), encoding="utf-8")

    monkeypatch.setenv("AI_API_KEYS", str(keys_path))
    monkeypatch.setattr(api_handler_module, "OpenAI", FakeOpenAI)

    handler = api_handler_module.ApiHandler()

    with pytest.raises(ValueError) as excinfo:
        handler.huggingface_request("Q", {"db": True}, "model-X")

    assert "Huggingface API key not found" in str(excinfo.value)