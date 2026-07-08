import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.handlers.tasks import TasksHandler


class FakeLogger:
    def __init__(self) -> None:
        self.info_calls: list[tuple[str, tuple]] = []

    def info(self, message: str, *args: object) -> None:
        self.info_calls.append((message, args))


def test_handle_with_empty_tasks_does_nothing(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.tasks.logger", fake_logger)

    handler = TasksHandler()
    handler.handle([])

    assert fake_logger.info_calls == []


def test_handle_logs_single_task(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.tasks.logger", fake_logger)

    handler = TasksHandler()
    task = {
        "title": "Finish PlannerOS",
        "priority": "high",
        "due": "2026-07-09",
        "description": "Complete TASK-001",
        "completed": False,
    }

    handler.handle([task])

    assert fake_logger.info_calls == [
        ("Creating task", ()),
        ("Title: %s", ("Finish PlannerOS",)),
        ("Priority: %s", ("high",)),
        ("Due: %s", ("2026-07-09",)),
        ("Description: %s", ("Complete TASK-001",)),
        ("Completed: %s", (False,)),
    ]


def test_handle_logs_multiple_tasks(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.tasks.logger", fake_logger)

    handler = TasksHandler()
    tasks = [
        {
            "title": "Finish PlannerOS",
            "priority": "high",
            "due": "2026-07-09",
            "description": "Complete TASK-001",
            "completed": False,
        },
        {
            "title": "Write docs",
            "priority": "medium",
            "due": "2026-07-10",
            "description": "Update README",
            "completed": True,
        },
    ]

    handler.handle(tasks)

    assert fake_logger.info_calls[0] == ("Creating task", ())
    assert fake_logger.info_calls[6] == ("Creating task", ())
    assert len(fake_logger.info_calls) == 12


def test_handle_calls_logger_expected_number_of_times(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.tasks.logger", fake_logger)

    handler = TasksHandler()
    tasks = [{"title": "Task A"}, {"title": "Task B"}, {"title": "Task C"}]

    handler.handle(tasks)

    assert len(fake_logger.info_calls) == len(tasks) * 6
