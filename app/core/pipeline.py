"""Execution pipeline coordinating clipboard, parser, and dispatcher."""

from app.clipboard.clipboard import Clipboard
from app.core.dispatcher import dispatch
from app.exceptions.planner_exceptions import PlannerError
from app.parser.parser import PlannerParser
from app.utils.logging import get_logger

logger = get_logger("planneros.core.pipeline")


class PlannerPipeline:
    """Coordinates reading, parsing, and dispatching a planner command.

    Contains no business logic of its own; it only sequences the
    Clipboard, PlannerParser, and Dispatcher modules.
    """

    def __init__(self) -> None:
        self._clipboard = Clipboard()
        self._parser = PlannerParser()

    def run(self) -> None:
        """Read the clipboard, parse it, and dispatch the resulting command."""
        try:
            text = self._clipboard.get_text()
            command = self._parser.parse(text)
            dispatch(command)
        except PlannerError:
            logger.exception("Planner pipeline failed")
