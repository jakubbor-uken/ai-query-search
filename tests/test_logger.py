import os
import sys
import logging
import types

import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import logger as logger_module


def test_logger_basic_config(monkeypatch):
    called = {}

    def fake_basicConfig(**kwargs):
        called["kwargs"] = kwargs

    def fake_addLevelName(level, name):
        called["level_name"] = (level, name)

    monkeypatch.setattr(logging, "basicConfig", fake_basicConfig)
    monkeypatch.setattr(logging, "addLevelName", fake_addLevelName)

    logger_module.Logger()

    assert "kwargs" in called
    cfg = called["kwargs"]

    assert cfg["level"] == logging.INFO

    fmt = cfg["format"]
    assert "%(asctime)s" in fmt
    assert "%(levelname)s" in fmt
    assert "%(filename)s" in fmt
    assert "%(lineno)d" in fmt
    assert "%(message)s" in fmt

    assert cfg["datefmt"] == "%Y-%m-%d %H:%M:%S"

    handlers = cfg["handlers"]
    assert isinstance(handlers, list)
    assert len(handlers) == 2

    assert called["level_name"] == (25, "INIT")


def test_logger_adds_init_method_and_level(caplog):
    with caplog.at_level(25):
        logger_module.Logger()

    assert hasattr(logging.Logger, "init")
    assert isinstance(logging.Logger.init, types.FunctionType)

    assert logging.getLevelName(25) == "INIT"

    test_logger = logging.getLogger("test_init_level")

    with caplog.at_level(25, logger="test_init_level"):
        test_logger.init("Init message from test")

    record = next(
        r for r in caplog.records
        if r.name == "test_init_level" and r.msg == "Init message from test"
    )

    assert record.levelno == 25
    assert record.levelname == "INIT"


def test_logger_logs_initial_message(caplog):
    with caplog.at_level(25, logger="logger"):
        logger_module.Logger()

    init_records = [
        r for r in caplog.records
        if r.name == "logger"
        and r.levelno == 25
        and r.levelname == "INIT"
        and r.msg == "Logging initialized"
    ]

    assert init_records, "Expected an INIT-level 'Logging initialized' record"