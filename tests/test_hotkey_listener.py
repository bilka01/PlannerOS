import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.hotkeys.listener import HOTKEY, HotkeyListener


class FakeKeyboard:
    def __init__(self) -> None:
        self.callback: Callable[[], None] | None = None
        self.handle = object()
        self.registered_hotkey: str | None = None
        self.removed_hotkeys: list[object] = []

    def add_hotkey(self, hotkey: str, callback: Callable[[], None]) -> object:
        self.registered_hotkey = hotkey
        self.callback = callback
        return self.handle

    def remove_hotkey(self, hotkey: object) -> None:
        self.removed_hotkeys.append(hotkey)


class FakePipeline:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error
        self.run_count = 0

    def run(self) -> None:
        self.run_count += 1

        if self.error is not None:
            raise self.error


class FakeLogger:
    def __init__(self) -> None:
        self.exceptions: list[str] = []

    def info(self, message: str, *args: object) -> None:
        pass

    def exception(self, message: str, *args: object) -> None:
        self.exceptions.append(message)


def test_start_registers_hotkey() -> None:
    keyboard = FakeKeyboard()
    pipeline = FakePipeline()
    listener = HotkeyListener(pipeline=pipeline, keyboard_module=keyboard)

    listener.start()

    assert keyboard.registered_hotkey == HOTKEY
    assert keyboard.callback is not None


def test_hotkey_callback_invokes_pipeline_run() -> None:
    keyboard = FakeKeyboard()
    pipeline = FakePipeline()
    listener = HotkeyListener(pipeline=pipeline, keyboard_module=keyboard)

    listener.start()
    assert keyboard.callback is not None
    keyboard.callback()

    assert pipeline.run_count == 1


def test_stop_removes_registered_hotkey() -> None:
    keyboard = FakeKeyboard()
    pipeline = FakePipeline()
    listener = HotkeyListener(pipeline=pipeline, keyboard_module=keyboard)

    listener.start()
    listener.stop()

    assert keyboard.removed_hotkeys == [keyboard.handle]


def test_stop_without_start_is_clean() -> None:
    keyboard = FakeKeyboard()
    pipeline = FakePipeline()
    listener = HotkeyListener(pipeline=pipeline, keyboard_module=keyboard)

    listener.stop()

    assert keyboard.removed_hotkeys == []


def test_hotkey_callback_errors_are_handled(monkeypatch) -> None:
    keyboard = FakeKeyboard()
    pipeline = FakePipeline(error=RuntimeError("boom"))
    fake_logger = FakeLogger()
    listener = HotkeyListener(pipeline=pipeline, keyboard_module=keyboard)

    monkeypatch.setattr("app.hotkeys.listener.logger", fake_logger)

    listener.start()
    assert keyboard.callback is not None
    keyboard.callback()

    assert pipeline.run_count == 1
    assert fake_logger.exceptions == ["Hotkey callback failed"]
