import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.handlers.obsidian import ObsidianHandler


class FakeLogger:
    def __init__(self) -> None:
        self.info_calls: list[tuple[str, tuple]] = []

    def info(self, message: str, *args: object) -> None:
        self.info_calls.append((message, args))


def test_handle_with_empty_payload_does_nothing(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.obsidian.logger", fake_logger)

    handler = ObsidianHandler()
    handler.handle({})

    assert fake_logger.info_calls == []


def test_handle_logs_single_note(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.obsidian.logger", fake_logger)

    handler = ObsidianHandler()
    obsidian = {
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-08.md",
        "content": ["- Finish PlannerOS MVP"],
    }

    handler.handle(obsidian)

    assert fake_logger.info_calls == [
        ("Updating Obsidian note", ()),
        ("Vault:", ()),
        ("Folder:", ()),
        ("Note:", ()),
        ("Content:", ()),
        ("- Finish PlannerOS MVP", ()),
    ]


def test_handle_logs_multiple_content_items(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.obsidian.logger", fake_logger)

    handler = ObsidianHandler()
    obsidian = {
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-08.md",
        "content": ["- Finish PlannerOS MVP", "- Review PR"],
    }

    handler.handle(obsidian)

    assert fake_logger.info_calls[0] == ("Updating Obsidian note", ())
    assert fake_logger.info_calls[5] == ("- Finish PlannerOS MVP", ())
    assert fake_logger.info_calls[6] == ("- Review PR", ())
    assert len(fake_logger.info_calls) == 7


def test_handle_calls_logger_expected_number_of_times(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.obsidian.logger", fake_logger)

    handler = ObsidianHandler()
    obsidian = {
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-08.md",
        "content": ["A", "B", "C"],
    }

    handler.handle(obsidian)

    assert len(fake_logger.info_calls) == 8
