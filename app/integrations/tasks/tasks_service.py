"""Filesystem-backed Markdown task writing service."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from app.exceptions.planner_exceptions import TasksWriteError
from app.utils.logging import get_logger

logger = get_logger("planneros.tasks_service")


class TasksService:
    """Create and update a Markdown task file on disk."""

    def __init__(self, file_path: str | None = None) -> None:
        self._file_path = Path(file_path or os.getenv("PLANNEROS_TASKS_FILE") or "~/Documents/PlannerOS/tasks.md").expanduser()

    def write_tasks(self, tasks: list[dict[str, Any]]) -> None:
        """Create or append tasks to the configured markdown file."""
        if not tasks:
            return

        logger.info("Opening task file...")
        try:
            self._file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise TasksWriteError("Unable to create task file directory") from exc

        try:
            if not self._file_path.exists():
                logger.info("Creating task file...")
                self._file_path.write_text(self._render_header(), encoding="utf-8")
            else:
                logger.info("Appending tasks...")
                existing_content = self._file_path.read_text(encoding="utf-8")
                if existing_content and not existing_content.endswith("\n"):
                    existing_content += "\n"
                self._file_path.write_text(existing_content.rstrip("\n") + "\n\n", encoding="utf-8")
        except OSError as exc:
            raise TasksWriteError("Unable to write task file") from exc

        try:
            self._append_tasks(tasks)
        except OSError as exc:
            raise TasksWriteError("Unable to append tasks") from exc

        logger.info("Tasks written successfully.")

    def _append_tasks(self, tasks: list[dict[str, Any]]) -> None:
        existing_content = self._file_path.read_text(encoding="utf-8") if self._file_path.exists() else ""
        sections = [self._format_task(task) for task in tasks]
        content = existing_content.rstrip("\n")
        if content:
            content += "\n\n"
        content += "\n\n".join(sections)
        self._file_path.write_text(content, encoding="utf-8")

    def _render_header(self) -> str:
        return "# Tasks"

    def _format_task(self, task: dict[str, Any]) -> str:
        title = str(task.get("title", ""))
        completed = bool(task.get("completed", False))
        checkbox = "[x]" if completed else "[ ]"
        lines = [f"- {checkbox} {title}"]

        priority = task.get("priority")
        if priority:
            lines.append(f"  - Priority: {priority}")

        due = task.get("due")
        if due:
            lines.append(f"  - Due: {due}")

        description = task.get("description")
        if description:
            lines.append(f"  - Description: {description}")

        return "\n".join(lines)
