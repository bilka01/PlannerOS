from __future__ import annotations

from typing import Any

from app.core.pipeline import PlannerPipeline
from app.utils.logging import get_logger

logger = get_logger("planneros.hotkeys.listener")

HOTKEY = "ctrl+shift+p"


class HotkeyListener:
    """Registers the global import hotkey and runs the planner pipeline."""

    def __init__(
        self,
        pipeline: PlannerPipeline | None = None,
        keyboard_module: Any | None = None,
    ) -> None:
        if keyboard_module is None:
            import keyboard as keyboard_module

        self._pipeline = pipeline if pipeline is not None else PlannerPipeline()
        self._keyboard = keyboard_module
        self._hotkey_handle: object | None = None

    def start(self) -> None:
        """Register the hotkey and begin listening for it."""
        self._hotkey_handle = self._keyboard.add_hotkey(HOTKEY, self._on_hotkey)
        logger.info("Listening for %s", HOTKEY)

    def stop(self) -> None:
        """Unregister the hotkey, if one is currently registered."""
        if self._hotkey_handle is not None:
            self._keyboard.remove_hotkey(self._hotkey_handle)
            self._hotkey_handle = None

    def _on_hotkey(self) -> None:
        """Run the planner pipeline, logging any failure without crashing."""
        try:
            self._pipeline.run()
        except Exception:
            logger.exception("Hotkey callback failed")


def start_listener() -> None:
    """Start the default global hotkey listener."""
    import keyboard

    listener = HotkeyListener(keyboard_module=keyboard)
    try:
        listener.start()
    except ImportError:
        logger.exception("Failed to start hotkey listener")
        return

    keyboard.wait()
