import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.pipeline import PlannerPipeline
from app.parser.schema import PlannerCommand

CLIPBOARD_TEXT = """
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


class FakeClipboard:
    def get_text(self) -> str:
        return CLIPBOARD_TEXT


def test_pipeline_reads_parses_and_dispatches(monkeypatch) -> None:
    calls: list[str] = []
    dispatched: list[PlannerCommand] = []

    def fake_dispatch(command: PlannerCommand) -> None:
        calls.append("dispatch")
        dispatched.append(command)

    monkeypatch.setattr("app.core.pipeline.Clipboard", FakeClipboard)
    monkeypatch.setattr("app.core.pipeline.dispatch", fake_dispatch)

    pipeline = PlannerPipeline()
    pipeline.run()

    assert calls == ["dispatch"]
    assert dispatched[0].type == "daily_plan"


def test_pipeline_handles_clipboard_errors(monkeypatch) -> None:
    from app.exceptions.planner_exceptions import ClipboardError

    class FailingClipboard:
        def get_text(self) -> str:
            raise ClipboardError("Failed to read clipboard contents.")

    monkeypatch.setattr("app.core.pipeline.Clipboard", FailingClipboard)

    pipeline = PlannerPipeline()

    pipeline.run()


def test_pipeline_handles_parser_errors(monkeypatch) -> None:
    class InvalidClipboard:
        def get_text(self) -> str:
            return "No planner block here."

    monkeypatch.setattr("app.core.pipeline.Clipboard", InvalidClipboard)

    pipeline = PlannerPipeline()

    pipeline.run()
