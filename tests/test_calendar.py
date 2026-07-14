import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.handlers.calendar import CalendarHandler


class FakeLogger:
    def __init__(self) -> None:
        self.info_calls: list[tuple[str, tuple]] = []

    def info(self, message: str, *args: object) -> None:
        self.info_calls.append((message, args))


class FakeCalendarService:
    def __init__(self) -> None:
        self.created_events: list[dict] = []

    def create_event(self, event: dict) -> dict:
        self.created_events.append(event)
        return {"id": f"event-{len(self.created_events)}"}


def test_handle_with_empty_events_does_nothing(monkeypatch) -> None:
    fake_logger = FakeLogger()
    fake_service = FakeCalendarService()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler(service=fake_service)
    handler.handle([])

    assert fake_service.created_events == []
    assert fake_logger.info_calls == []


def test_handle_delegates_single_event_to_service(monkeypatch) -> None:
    fake_logger = FakeLogger()
    fake_service = FakeCalendarService()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler(service=fake_service)
    event = {
        "title": "Doctor Appointment",
        "start": "2026-07-10T09:00",
        "end": "2026-07-10T10:00",
        "location": "Clinic",
        "description": "Annual checkup",
    }

    handler.handle([event])

    assert fake_service.created_events == [event]
    assert fake_logger.info_calls == [
        ("Creating calendar event...", ()),
        ("Calendar event created successfully. Event id: %s", ("event-1",)),
    ]


def test_handle_delegates_multiple_events_to_service(monkeypatch) -> None:
    fake_logger = FakeLogger()
    fake_service = FakeCalendarService()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler(service=fake_service)
    events = [
        {"title": "Doctor Appointment"},
        {"title": "Team Standup"},
    ]

    handler.handle(events)

    assert fake_service.created_events == events
    assert fake_logger.info_calls == [
        ("Creating calendar event...", ()),
        ("Calendar event created successfully. Event id: %s", ("event-1",)),
        ("Creating calendar event...", ()),
        ("Calendar event created successfully. Event id: %s", ("event-2",)),
    ]
