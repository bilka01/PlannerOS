from app.utils.logging import get_logger

logger = get_logger("planneros.tasks")


class TasksHandler:
    """Log tasks that PlannerOS would create.

    This is an MVP handler: it performs no schema validation and makes no
    external calls. Its only responsibility is to log what would be executed.
    """

    def handle(self, tasks: list[dict]) -> None:
        """Log each task that would be created.

        Args:
            tasks: Already validated task dictionaries.
        """
        if not tasks:
            return

        for task in tasks:
            logger.info("Creating task")
            logger.info("Title: %s", task.get("title"))
            logger.info("Priority: %s", task.get("priority"))
            logger.info("Due: %s", task.get("due"))
            logger.info("Description: %s", task.get("description"))
            logger.info("Completed: %s", task.get("completed"))

