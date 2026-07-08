import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core import dispatcher
from app.parser.parser import PlannerParser
from app.parser.schema import PlannerCommand


def test_dispatch_invokes_handlers_for_non_empty_command_sections(
    monkeypatch,
) -> None:
    received: list[tuple[str, object]] = []

    def fake_calendar_handler(events: list[dict]) -> None:
        received.append(("calendar", events))

    def fake_tasks_handler(command: PlannerCommand) -> None:
        received.append(("tasks", command))

    def fake_obsidian_handler(command: PlannerCommand) -> None:
        received.append(("obsidian", command))

    monkeypatch.setattr(dispatcher.calendar_handler, "handle", fake_calendar_handler)
    monkeypatch.setattr(dispatcher, "handle_tasks", fake_tasks_handler)
    monkeypatch.setattr(dispatcher, "handle_obsidian", fake_obsidian_handler)

    clipboard_text = """
    Daily plan:

    <!-- AI_PLANNER_START -->
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [{"title": "Study SQL"}],
        "tasks": [{"title": "Apply for jobs"}],
        "obsidian": {"note": "Daily plan"}
    }
    <!-- AI_PLANNER_END -->
    """

    command = PlannerParser().parse(clipboard_text)

    dispatcher.dispatch(command)

    assert received == [
        ("calendar", command.calendar),
        ("tasks", command),
        ("obsidian", command),
    ]


def test_dispatch_skips_handlers_for_empty_command_sections(monkeypatch) -> None:
    received: list[str] = []

    def fake_calendar_handler(events: list[dict]) -> None:
        received.append("calendar")

    def fake_tasks_handler(command: PlannerCommand) -> None:
        received.append("tasks")

    def fake_obsidian_handler(command: PlannerCommand) -> None:
        received.append("obsidian")

    monkeypatch.setattr(dispatcher.calendar_handler, "handle", fake_calendar_handler)
    monkeypatch.setattr(dispatcher, "handle_tasks", fake_tasks_handler)
    monkeypatch.setattr(dispatcher, "handle_obsidian", fake_obsidian_handler)

    clipboard_text = """
    <!-- AI_PLANNER_START -->
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [],
        "tasks": [],
        "obsidian": {}
    }
    <!-- AI_PLANNER_END -->
    """
    command = PlannerParser().parse(clipboard_text)

    dispatcher.dispatch(command)

    assert received == []
