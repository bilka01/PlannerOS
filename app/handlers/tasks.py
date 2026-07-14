from app.integrations.tasks.tasks_service import TasksService
from app.utils.logging import get_logger

logger = get_logger("planneros.tasks")


class TasksHandler:
    """Orchestrate task writing through the service layer."""

    def __init__(self, service: TasksService | None = None) -> None:
        self._service = service if service is not None else TasksService()

    def handle(self, tasks: list[dict]) -> None:
        """Write tasks to disk through the service layer.

        Args:
            tasks: Already validated task dictionaries.
        """
        if not tasks:
            return

        logger.info("Opening task file...")
        self._service.write_tasks(tasks)

