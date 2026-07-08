import inspect
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.clipboard.clipboard import Clipboard
from app.exceptions.planner_exceptions import ClipboardError, PlannerError


class FakeClipboardBackend:
    def __init__(self, text: str = "", error: Exception | None = None) -> None:
        self.text = text
        self.error = error

    def paste(self) -> str:
        if self.error is not None:
            raise self.error

        return self.text


class FakeLogger:
    def __init__(self) -> None:
        self.exceptions: list[str] = []

    def exception(self, message: str, *args: object) -> None:
        self.exceptions.append(message)


def use_fake_pyperclip(monkeypatch, backend: FakeClipboardBackend) -> None:
    def fake_import_module(module_name: str) -> FakeClipboardBackend:
        assert module_name == "pyperclip"
        return backend

    monkeypatch.setattr("app.clipboard.clipboard.import_module", fake_import_module)


def test_get_text_returns_clipboard_text(monkeypatch) -> None:
    use_fake_pyperclip(monkeypatch, FakeClipboardBackend("Plan for today"))
    clipboard = Clipboard()

    assert clipboard.get_text() == "Plan for today"


def test_get_text_returns_empty_clipboard_text(monkeypatch) -> None:
    use_fake_pyperclip(monkeypatch, FakeClipboardBackend(""))
    clipboard = Clipboard()

    assert clipboard.get_text() == ""


def test_get_text_returns_unicode_text(monkeypatch) -> None:
    use_fake_pyperclip(monkeypatch, FakeClipboardBackend("štúdium SQL"))
    clipboard = Clipboard()

    assert clipboard.get_text() == "štúdium SQL"


def test_get_text_returns_multiline_text(monkeypatch) -> None:
    text = "Line one\nLine two\nLine three"
    use_fake_pyperclip(monkeypatch, FakeClipboardBackend(text))
    clipboard = Clipboard()

    assert clipboard.get_text() == text


def test_get_text_raises_clipboard_error_on_access_failure(monkeypatch) -> None:
    fake_logger = FakeLogger()
    use_fake_pyperclip(monkeypatch, FakeClipboardBackend(error=RuntimeError("boom")))
    clipboard = Clipboard()

    monkeypatch.setattr("app.clipboard.clipboard.logger", fake_logger)

    with pytest.raises(ClipboardError):
        clipboard.get_text()

    assert fake_logger.exceptions == ["Failed to read clipboard text"]


def test_clipboard_error_extends_planner_error() -> None:
    assert issubclass(ClipboardError, PlannerError)


def test_clipboard_public_api_has_one_public_method() -> None:
    public_methods = [
        name
        for name, value in inspect.getmembers(Clipboard, inspect.isfunction)
        if not name.startswith("_")
    ]

    assert public_methods == ["get_text"]
