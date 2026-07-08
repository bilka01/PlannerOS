from importlib import import_module

from app.exceptions.planner_exceptions import ClipboardError
from app.utils.logging import get_logger

logger = get_logger("planneros.clipboard")


class Clipboard:
    """Reads text from the system clipboard."""

    def get_text(self) -> str:
        """Return the current clipboard contents as text."""
        try:
            pyperclip = import_module("pyperclip")
            return pyperclip.paste()
        except Exception as error:
            logger.exception("Failed to read clipboard text")
            raise ClipboardError("Failed to read clipboard text.") from error