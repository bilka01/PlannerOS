"""Calendar handler for PlannerOS."""

from __future__ import annotations

from typing import Any

from app.integrations.google.calendar_service import GoogleCalendarService
from app.utils.logging import get_logger

logger = get_logger("planneros.calendar")


class CalendarHandler:
    """Orchestrate calendar event creation through the Google service."""

    def __init__(self, service: GoogleCalendarService | None = None) -> None:
        self._service = service if service is not None else GoogleCalendarService()

    def handle(self, events: list[dict[str, Any]]) -> None:
        """Create each validated calendar event through the service layer.

        Args:
            events: Already validated calendar event dictionaries.
        """
        if not events:
            return

        for event in events:
            logger.info("Creating calendar event...")
            created_event = self._service.create_event(event)
            logger.info(
                "Calendar event created successfully. Event id: %s",
                created_event.get("id"),
            )
