import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.exceptions.planner_exceptions import ObsidianVaultNotFoundError
from app.handlers.obsidian import ObsidianHandler
from app.integrations.obsidian.obsidian_service import ObsidianService


class FakeLogger:
    def __init__(self) -> None:
        self.info_calls: list[tuple[str, tuple]] = []

    def info(self, message: str, *args: object) -> None:
        self.info_calls.append((message, args))


def test_handle_with_empty_payload_does_nothing() -> None:
    calls: list[dict] = []

    class FakeService:
        def write_note(self, note: dict) -> None:
            calls.append(note)

    handler = ObsidianHandler(service=FakeService())
    handler.handle({})

    assert calls == []


def test_service_creates_folder_and_note(tmp_path, monkeypatch) -> None:
    vault_root = tmp_path / "obsidian-vault"
    vault_root.mkdir()
    monkeypatch.setenv("PLANNEROS_OBSIDIAN_VAULT", str(vault_root))

    service = ObsidianService()
    note_payload = {
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-15.md",
        "content": ["# Daily Notes", "", "- Finish PlannerOS"],
    }

    service.write_note(note_payload)

    note_path = vault_root / "PlannerOS" / "Daily" / "2026-07-15.md"
    assert note_path.exists()
    assert note_path.read_text(encoding="utf-8") == "# Daily Notes\n\n- Finish PlannerOS"


def test_service_raises_when_vault_missing(tmp_path, monkeypatch) -> None:
    missing_vault = tmp_path / "missing-vault"
    monkeypatch.setenv("PLANNEROS_OBSIDIAN_VAULT", str(missing_vault))

    service = ObsidianService()

    with pytest.raises(ObsidianVaultNotFoundError):
        service.write_note({"vault": "PlannerOS", "folder": "Daily", "note": "note.md", "content": ["Hello"]})


def test_service_appends_to_existing_note(tmp_path, monkeypatch) -> None:
    vault_root = tmp_path / "obsidian-vault"
    vault_root.mkdir()
    monkeypatch.setenv("PLANNEROS_OBSIDIAN_VAULT", str(vault_root))

    service = ObsidianService()
    note_path = vault_root / "PlannerOS" / "Daily"
    note_path.mkdir(parents=True)
    existing_note = note_path / "2026-07-15.md"
    existing_note.write_text("# Existing\n", encoding="utf-8")

    service.write_note({
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-15.md",
        "content": ["- Added line"],
    })

    assert existing_note.read_text(encoding="utf-8") == "# Existing\n\n- Added line"


def test_service_creates_empty_note_for_empty_content(tmp_path, monkeypatch) -> None:
    vault_root = tmp_path / "obsidian-vault"
    vault_root.mkdir()
    monkeypatch.setenv("PLANNEROS_OBSIDIAN_VAULT", str(vault_root))

    service = ObsidianService()
    service.write_note({"vault": "PlannerOS", "folder": "Daily", "note": "empty.md", "content": []})

    note_path = vault_root / "PlannerOS" / "Daily" / "empty.md"
    assert note_path.exists()
    assert note_path.read_text(encoding="utf-8") == ""


def test_service_writes_multiple_content_lines(tmp_path, monkeypatch) -> None:
    vault_root = tmp_path / "obsidian-vault"
    vault_root.mkdir()
    monkeypatch.setenv("PLANNEROS_OBSIDIAN_VAULT", str(vault_root))

    service = ObsidianService()
    service.write_note({
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-15.md",
        "content": ["Line 1", "Line 2", "Line 3"],
    })

    note_path = vault_root / "PlannerOS" / "Daily" / "2026-07-15.md"
    assert note_path.read_text(encoding="utf-8") == "Line 1\nLine 2\nLine 3"


def test_handler_delegates_to_service(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.obsidian.logger", fake_logger)
    captured: list[dict] = []

    class FakeService:
        def write_note(self, note: dict) -> None:
            captured.append(note)

    handler = ObsidianHandler(service=FakeService())
    obsidian = {"vault": "PlannerOS", "folder": "Daily", "note": "note.md", "content": ["Hello"]}

    handler.handle(obsidian)

    assert captured == [obsidian]
    assert fake_logger.info_calls[0][0] == "Opening Obsidian vault..."
