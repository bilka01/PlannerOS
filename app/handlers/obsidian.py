from app.integrations.obsidian.obsidian_service import ObsidianService
from app.utils.logging import get_logger

logger = get_logger("planneros.obsidian")


class ObsidianHandler:
    """Orchestrate Obsidian note updates through the service layer."""

    def __init__(self, service: ObsidianService | None = None) -> None:
        self._service = service if service is not None else ObsidianService()

    def handle(self, obsidian: dict) -> None:
        """Create or update an Obsidian note through the service.

        Args:
            obsidian: Already validated Obsidian instruction dictionary.
        """
        if not obsidian:
            return

        logger.info("Opening Obsidian vault...")
        self._service.write_note(obsidian)


def handle_obsidian(command: object) -> None:
    """Compatibility wrapper for the dispatcher interface."""
    handler = ObsidianHandler()
    handler.handle(command.obsidian)
