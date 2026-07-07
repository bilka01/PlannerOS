from app.parser.schema import PlannerCommand
from app.utils.logging import get_logger

logger = get_logger("planneros.handlers.tasks")


def handle_tasks(command: PlannerCommand) -> None:
    logger.info("Tasks Handler executed")
    logger.debug("Command received: %s", command)
