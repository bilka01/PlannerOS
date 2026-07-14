import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.exceptions.planner_exceptions import TasksWriteError
from app.handlers.tasks import TasksHandler
from app.integrations.tasks.tasks_service import TasksService


class FakeLogger:
    def __init__(self) -> None:
        self.info_calls: list[tuple[str, tuple]] = []

    def info(self, message: str, *args: object) -> None:
        self.info_calls.append((message, args))


def test_handle_with_empty_tasks_does_nothing() -> None:
    calls: list[list[dict]] = []

    class FakeService:
        def write_tasks(self, tasks: list[dict]) -> None:
            calls.append(tasks)

    handler = TasksHandler(service=FakeService())
    handler.handle([])

    assert calls == []


def test_service_creates_task_file_with_parent_directories(tmp_path, monkeypatch) -> None:
    target_file = tmp_path / "nested" / "planneros" / "tasks.md"
    monkeypatch.setenv("PLANNEROS_TASKS_FILE", str(target_file))

    service = TasksService()
    service.write_tasks([
        {
            "title": "Review PlannerOS pull requests",
            "priority": "High",
            "due": "2026-07-15",
            "description": "Review recent changes before merging.",
            "completed": False,
        }
    ])

    assert target_file.exists()
    assert target_file.read_text(encoding="utf-8") == (
        "# Tasks\n\n"
        "- [ ] Review PlannerOS pull requests\n"
        "  - Priority: High\n"
        "  - Due: 2026-07-15\n"
        "  - Description: Review recent changes before merging."
    )


def test_service_appends_to_existing_file(tmp_path, monkeypatch) -> None:
    target_file = tmp_path / "tasks.md"
    monkeypatch.setenv("PLANNEROS_TASKS_FILE", str(target_file))
    target_file.write_text("# Tasks\n\n- [ ] Existing item\n", encoding="utf-8")

    service = TasksService()
    service.write_tasks([
        {
            "title": "New task",
            "priority": "Medium",
            "due": "2026-07-16",
            "description": "Another task",
            "completed": False,
        }
    ])

    assert target_file.read_text(encoding="utf-8") == (
        "# Tasks\n\n"
        "- [ ] Existing item\n\n"
        "- [ ] New task\n"
        "  - Priority: Medium\n"
        "  - Due: 2026-07-16\n"
        "  - Description: Another task"
    )


def test_service_writes_empty_task_list_without_creating_content(tmp_path, monkeypatch) -> None:
    target_file = tmp_path / "tasks.md"
    monkeypatch.setenv("PLANNEROS_TASKS_FILE", str(target_file))

    service = TasksService()
    service.write_tasks([])

    assert not target_file.exists()


def test_service_writes_multiple_tasks(tmp_path, monkeypatch) -> None:
    target_file = tmp_path / "tasks.md"
    monkeypatch.setenv("PLANNEROS_TASKS_FILE", str(target_file))

    service = TasksService()
    service.write_tasks([
        {"title": "Task One", "priority": "Low", "due": "", "description": "", "completed": False},
        {"title": "Task Two", "priority": "High", "due": "", "description": "", "completed": True},
    ])

    content = target_file.read_text(encoding="utf-8")
    assert "- [ ] Task One" in content
    assert "- [x] Task Two" in content


def test_service_raises_write_error_on_unwritable_path(tmp_path, monkeypatch) -> None:
    target_file = tmp_path / "tasks.md"
    monkeypatch.setenv("PLANNEROS_TASKS_FILE", str(target_file))

    service = TasksService()
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text("existing", encoding="utf-8")
    target_file.chmod(0o444)

    with pytest.raises(TasksWriteError):
        service.write_tasks([{"title": "Task", "priority": "", "due": "", "description": "", "completed": False}])


def test_handler_delegates_to_service(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.tasks.logger", fake_logger)
    captured: list[list[dict]] = []

    class FakeService:
        def write_tasks(self, tasks: list[dict]) -> None:
            captured.append(tasks)

    handler = TasksHandler(service=FakeService())
    tasks = [{"title": "Task", "priority": "", "due": "", "description": "", "completed": False}]

    handler.handle(tasks)

    assert captured == [tasks]
    assert fake_logger.info_calls[0][0] == "Opening task file..."
