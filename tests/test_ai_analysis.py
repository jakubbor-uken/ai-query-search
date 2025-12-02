import os
import sys
import logging

import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import logger as logger_module
import ai_analysis as ai_analysis_module

class FakeQueryHandler:
    instances = []

    def __init__(self):
        self.loaded_dbs = []
        self.sent_queries = []
        FakeQueryHandler.instances.append(self)

    def load_database(self, path):
        self.loaded_dbs.append(path)

    def send_query(self, query, model):
        idx = len(self.sent_queries) + 1
        self.sent_queries.append((query, model))
        return {
            "msg": f"resp-{idx}-{query}-{model}",
            "elapsed_time": 0.01 * idx,
        }

def _setup_logging():
    logger_module.Logger()

def test_run_analysis_calls_queryhandler_for_each_combination(monkeypatch):
    _setup_logging()

    FakeQueryHandler.instances.clear()
    monkeypatch.setattr(ai_analysis_module, "QueryHandler", FakeQueryHandler)

    analyzer = ai_analysis_module.AI_Analysis()

    model_list = ["modelA", "modelB"]
    dbs_and_queries = [
        {"query": "Q1", "db": "/path/db1.json"},
        {"query": "Q2", "db": "/path/db2.json"},
    ]

    outputs = analyzer.run_analysis(model_list, dbs_and_queries)

    assert len(FakeQueryHandler.instances) == 1
    fake = FakeQueryHandler.instances[0]

    assert fake.loaded_dbs == [
        "/path/db1.json",
        "/path/db2.json",
        "/path/db1.json",
        "/path/db2.json",
    ]

    assert fake.sent_queries == [
        ("Q1", "modelA"),
        ("Q2", "modelA"),
        ("Q1", "modelB"),
        ("Q2", "modelB"),
    ]

    assert len(outputs) == 4
    for o in outputs:
        assert set(o.keys()) == {"output", "model", "query", "elapsed_time"}


def test_run_analysis_output_structure_and_values(monkeypatch):
    _setup_logging()
    FakeQueryHandler.instances.clear()
    monkeypatch.setattr(ai_analysis_module, "QueryHandler", FakeQueryHandler)

    analyzer = ai_analysis_module.AI_Analysis()

    model_list = ["M"]
    dbs_and_queries = [
        {"query": "Q1", "db": "/db1.json"},
        {"query": "Q2", "db": "/db2.json"},
    ]

    outputs = analyzer.run_analysis(model_list, dbs_and_queries)

    assert outputs == [
        {
            "output": "resp-1-Q1-M",
            "model": "M",
            "query": "Q1",
            "elapsed_time": 0.01,
        },
        {
            "output": "resp-2-Q2-M",
            "model": "M",
            "query": "Q2",
            "elapsed_time": 0.02,
        },
    ]


def test_run_analysis_writes_output_log(tmp_path, monkeypatch):
    _setup_logging()
    FakeQueryHandler.instances.clear()
    monkeypatch.setattr(ai_analysis_module, "QueryHandler", FakeQueryHandler)

    monkeypatch.chdir(tmp_path)

    analyzer = ai_analysis_module.AI_Analysis()

    model_list = ["modelA"]
    dbs_and_queries = [
        {"query": "Q1", "db": "/db1.json"},
        {"query": "Q2", "db": "/db2.json"},
    ]

    outputs = analyzer.run_analysis(model_list, dbs_and_queries)

    output_path = tmp_path / "output.log"
    assert output_path.exists()

    lines = output_path.read_text().splitlines()
    assert len(lines) == len(outputs)

    assert lines[0] == str(outputs[0])
    assert lines[1] == str(outputs[1])


def test_run_analysis_logs_informational_messages(monkeypatch, caplog):
    _setup_logging()
    FakeQueryHandler.instances.clear()
    monkeypatch.setattr(ai_analysis_module, "QueryHandler", FakeQueryHandler)

    analyzer = ai_analysis_module.AI_Analysis()

    model_list = ["M"]
    dbs_and_queries = [{"query": "Q1", "db": "/db1.json"}]

    with caplog.at_level(logging.INFO, logger="ai_analysis"):
        analyzer.run_analysis(model_list, dbs_and_queries)

    messages = [r.getMessage() for r in caplog.records]

    assert any("Running analysis" in m for m in messages)
    assert any("Loading model: M" in m for m in messages)
    assert any("Added output for model: M, query: Q1 to output_list" in m for m in messages)
    assert any("Saving analysis results to file:" in m for m in messages)