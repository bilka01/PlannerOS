import logging
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.utils import logging as planneros_logging


def _fake_paths(tmp_path: Path) -> dict[str, Path]:
    return {"logs": tmp_path / "logs"}


def _fake_ensure_directories(paths: dict[str, Path]) -> None:
    paths["logs"].mkdir(parents=True, exist_ok=True)


@pytest.fixture(autouse=True)
def _cleanup_test_loggers():
    yield
    for name in list(logging.Logger.manager.loggerDict.keys()):
        if name.startswith("test.logger."):
            logger = logging.getLogger(name)
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)


def test_get_logger_returns_configured_logger(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(planneros_logging, "get_project_paths", lambda: _fake_paths(tmp_path))
    monkeypatch.setattr(planneros_logging, "ensure_directories", _fake_ensure_directories)

    logger = planneros_logging.get_logger("test.logger.returns")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test.logger.returns"
    assert logger.level == logging.INFO


def test_get_logger_avoids_duplicate_handlers(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(planneros_logging, "get_project_paths", lambda: _fake_paths(tmp_path))
    monkeypatch.setattr(planneros_logging, "ensure_directories", _fake_ensure_directories)

    first = planneros_logging.get_logger("test.logger.duplicate")
    handler_count = len(first.handlers)

    second = planneros_logging.get_logger("test.logger.duplicate")

    assert second is first
    assert len(second.handlers) == handler_count


def test_get_logger_creates_log_directory(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(planneros_logging, "get_project_paths", lambda: _fake_paths(tmp_path))
    monkeypatch.setattr(planneros_logging, "ensure_directories", _fake_ensure_directories)

    planneros_logging.get_logger("test.logger.directory")

    assert (tmp_path / "logs").exists()


def test_get_logger_creates_log_file_after_writing(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(planneros_logging, "get_project_paths", lambda: _fake_paths(tmp_path))
    monkeypatch.setattr(planneros_logging, "ensure_directories", _fake_ensure_directories)

    logger = planneros_logging.get_logger("test.logger.file")
    logger.info("hello world")

    for handler in logger.handlers:
        handler.flush()

    log_file = tmp_path / "logs" / "planneros.log"
    assert log_file.exists()
    assert "hello world" in log_file.read_text()