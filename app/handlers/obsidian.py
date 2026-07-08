from app.utils.logging import get_logger

logger = get_logger("planneros.obsidian")


class ObsidianHandler:
    """Log Obsidian updates that PlannerOS would create.

    This is an MVP handler: it performs no schema validation and makes no
    external calls. Its only responsibility is to log what would be executed.
    """

    def handle(self, obsidian: dict) -> None:
        """Log each Obsidian update that would be executed.

        Args:
            obsidian: Already validated Obsidian instruction dictionary.
        """
        if not obsidian:
            return

        logger.info("Updating Obsidian note")
        logger.info("Vault:")
        logger.info("Folder:")
        logger.info("Note:")
        logger.info("Content:")

        content = obsidian.get("content")
        if isinstance(content, list):
            for item in content:
                logger.info(item)


def handle_obsidian(command: object) -> None:
    """Compatibility wrapper for the dispatcher interface."""
    handler = ObsidianHandler()
    handler.handle(command.obsidian)
