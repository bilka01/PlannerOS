import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.handlers.calendar import CalendarHandler


class FakeLogger:
    def __init__(self) -> None:
        self.info_calls: list[tuple[str, tuple]] = []

    def info(self, message: str, *args: object) -> None:
        self.info_calls.append((message, args))


def test_handle_with_empty_events_does_nothing(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler()
    handler.handle([])

    assert fake_logger.info_calls == []


def test_handle_logs_single_event(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler()
    event = {
        "title": "Doctor Appointment",
        "start": "2026-07-10T09:00",
        "end": "2026-07-10T10:00",
        "location": "Clinic",
        "description": "Annual checkup",
    }

    handler.handle([event])

    assert fake_logger.info_calls == [
        ("Creating calendar event", ()),
        ("Title: %s", ("Doctor Appointment",)),
        ("Start: %s", ("2026-07-10T09:00",)),
        ("End: %s", ("2026-07-10T10:00",)),
        ("Location: %s", ("Clinic",)),
        ("Description: %s", ("Annual checkup",)),
    ]


def test_handle_logs_multiple_events(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler()
    events = [
        {
            "title": "Doctor Appointment",
            "start": "2026-07-10T09:00",
            "end": "2026-07-10T10:00",
            "location": "Clinic",
            "description": "Annual checkup",
        },
        {
            "title": "Team Standup",
            "start": "2026-07-10T11:00",
            "end": "2026-07-10T11:15",
            "location": "Office",
            "description": "Daily sync",
        },
    ]

    handler.handle(events)

    assert fake_logger.info_calls[0] == ("Creating calendar event", ())
    assert fake_logger.info_calls[6] == ("Creating calendar event", ())
    assert len(fake_logger.info_calls) == 12


def test_handle_calls_logger_expected_number_of_times(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler()
    events = [{"title": "Event A"}, {"title": "Event B"}, {"title": "Event C"}]

    handler.handle(events)

    assert len(fake_logger.info_calls) == len(events) * 6


def test_handler_with_single_event_logs_expected_output(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler()
    events = [{"title": "Doctor Appointment"}]

    handler.handle(events)

    assert fake_logger.info_calls[0] == ("Creating calendar event", ())
    assert len(fake_logger.info_calls) == 6


def test_handler_with_empty_events_does_nothing(monkeypatch) -> None:
    fake_logger = FakeLogger()
    monkeypatch.setattr("app.handlers.calendar.logger", fake_logger)

    handler = CalendarHandler()

    handler.handle([])

    assert fake_logger.info_calls == []