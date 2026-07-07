from app.parser.schema import PlannerCommand
from app.utils.logging import get_logger

logger = get_logger("planneros.handlers.calendar")


def handle_calendar(command: PlannerCommand) -> None:
    logger.info("Calendar Handler executed")
    logger.debug("Command received: %s", command)
