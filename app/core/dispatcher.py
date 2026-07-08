from app.config import ensure_directories, get_project_paths
from app.handlers.calendar import CalendarHandler
from app.handlers.obsidian import handle_obsidian
from app.handlers.tasks import handle_tasks
from app.parser.schema import PlannerCommand
from app.utils.logging import get_logger

logger = get_logger("planneros.dispatcher")
calendar_handler = CalendarHandler()


def dispatch(command: PlannerCommand) -> None:
    paths = get_project_paths()
    ensure_directories(paths)

    logger.info("Dispatching planner command: %s", command.type)

    if command.calendar:
        calendar_handler.handle(command.calendar)

    if command.tasks:
        handle_tasks(command)

    if command.obsidian:
        handle_obsidian(command)
