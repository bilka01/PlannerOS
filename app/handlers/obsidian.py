from app.parser.schema import PlannerCommand
from app.utils.logging import get_logger

logger = get_logger("planneros.handlers.obsidian")


def handle_obsidian(command: PlannerCommand) -> None:
    logger.info("Obsidian Handler executed")
    logger.debug("Command received: %s", command)
