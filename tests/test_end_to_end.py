import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.pipeline import PlannerPipeline
from app.core import dispatcher


PLANNER_BLOCK = """
Daily plan:

<!-- AI_PLANNER_START -->
{
    "version": 1,
    "type": "daily_plan",
    "calendar": [
        {
            "title": "Interview",
            "start": "2026-07-10T09:00",
            "end": "2026-07-10T10:00",
            "location": "Microsoft Teams",
            "description": "Data Analyst interview"
        }
    ],
    "tasks": [
        {
            "title": "Update CV",
            "priority": "high",
            "due": "2026-07-10",
            "description": "Tailor CV for interview",
            "completed": false
        }
    ],
    "obsidian": {
        "vault": "PlannerOS",
        "folder": "Daily",
        "note": "2026-07-10.md",
        "content": [
            "- Prepare interview",
            "- Review SQL notes"
        ]
    }
}
<!-- AI_PLANNER_END -->
"""


def test_end_to_end_integration(monkeypatch) -> None:
    # Mock clipboard.get_text() and record call count
    clipboard_calls = {"count": 0}

    def fake_get_text(self) -> str:
        clipboard_calls["count"] += 1
        return PLANNER_BLOCK

    monkeypatch.setattr("app.clipboard.clipboard.Clipboard.get_text", fake_get_text)

    # Capture handler inputs
    received = {}

    def fake_calendar_handle(events: list[dict]) -> None:
        received["calendar"] = events

    def fake_tasks_handle(tasks: list[dict]) -> None:
        received["tasks"] = tasks

    def fake_obsidian_handle(obsidian: dict) -> None:
        received["obsidian"] = obsidian

    # Patch dispatcher handlers (they are module-level instances)
    monkeypatch.setattr(dispatcher.calendar_handler, "handle", fake_calendar_handle)
    monkeypatch.setattr(dispatcher.tasks_handler, "handle", fake_tasks_handle)
    monkeypatch.setattr(dispatcher.obsidian_handler, "handle", fake_obsidian_handle)

    # Run the real pipeline
    PlannerPipeline().run()

    # Verifications
    assert clipboard_calls["count"] == 1, "Clipboard.get_text() should be called once"

    # Calendar
    assert "calendar" in received, "CalendarHandler.handle() was not called"
    assert isinstance(received["calendar"], list)
    assert received["calendar"][0]["title"] == "Interview"
    assert received["calendar"][0]["location"] == "Microsoft Teams"

    # Tasks
    assert "tasks" in received, "TasksHandler.handle() was not called"
    assert isinstance(received["tasks"], list)
    assert received["tasks"][0]["title"] == "Update CV"
    assert received["tasks"][0]["priority"] == "high"

    # Obsidian
    assert "obsidian" in received, "ObsidianHandler.handle() was not called"
    assert isinstance(received["obsidian"], dict)
    assert received["obsidian"]["vault"] == "PlannerOS"
    assert received["obsidian"]["content"] == ["- Prepare interview", "- Review SQL notes"]
