import keyboard

from app.clipboard.clipboard import get_clipboard_text
from app.core.dispatcher import dispatch
from app.parser.parser import PlannerParser
from app.utils.logging import get_logger

logger = get_logger("planneros.hotkeys.listener")


def import_plan() -> None:
    try:
        text = get_clipboard_text()
        command = PlannerParser().parse(text)
        dispatch(command)
        logger.info("Plan imported successfully")
    except Exception as exc:
        logger.exception("Failed to import plan: %s", exc)


def start_listener() -> None:
    keyboard.add_hotkey("ctrl+shift+p", import_plan)
    logger.info("Listening for Ctrl+Shift+P")
    keyboard.wait()
