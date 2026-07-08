"""Calendar handler for PlannerOS.

MVP implementation: receives already-validated calendar events and logs
what would be created. There is no integration with Google Calendar or
any other external service yet.
"""

from app.utils.logging import get_logger

logger = get_logger("planneros.calendar")


class CalendarHandler:
    """Logs calendar events that PlannerOS would create.

    This is an MVP handler: it performs no schema validation (the parser
    already validated the data) and makes no external calls. Its only
    responsibility is to log what would be executed.
    """
    def handle(self, events: list[dict]) -> None:
        """Log each calendar event that would be created.

        Args:
            events: Already validated calendar event dictionaries.
        """
        for event in events:
            logger.info("Creating calendar event")
            logger.info("Title: %s", event.get("title"))
            logger.info("Start: %s", event.get("start"))
            logger.info("End: %s", event.get("end"))
            logger.info("Location: %s", event.get("location"))
            logger.info("Description: %s", event.get("description"))
