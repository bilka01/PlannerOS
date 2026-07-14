"""Filesystem-backed Obsidian note writing service."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from app.exceptions.planner_exceptions import ObsidianVaultNotFoundError, ObsidianWriteError
from app.utils.logging import get_logger

logger = get_logger("planneros.obsidian_service")


class ObsidianService:
    """Create and update Markdown notes inside an Obsidian vault."""

    def __init__(self, vault_root: str | None = None) -> None:
        self._vault_root = Path(vault_root or os.getenv("PLANNEROS_OBSIDIAN_VAULT") or "~/Documents/ObsidianVault").expanduser()

    def write_note(self, note: dict[str, Any]) -> None:
        """Create or update a markdown note in the configured vault."""
        if not note:
            return

        logger.info("Opening Obsidian vault...")
        if not self._vault_root.exists():
            raise ObsidianVaultNotFoundError("Obsidian vault does not exist")

        vault_name = note.get("vault")
        folder_name = note.get("folder")
        note_name = note.get("note")
        content = note.get("content", [])

        if not vault_name or not note_name:
            raise ObsidianWriteError("Obsidian note payload is missing required fields")

        vault_path = self._vault_root / str(vault_name)
        folder_path = vault_path / str(folder_name) if folder_name else vault_path

        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info("Creating folder...")
        except OSError as exc:
            raise ObsidianWriteError("Unable to create Obsidian folder") from exc

        note_path = folder_path / str(note_name)

        try:
            if note_path.exists():
                logger.info("Appending content...")
                existing_content = note_path.read_text(encoding="utf-8")
                new_content = self._join_content(existing_content, content)
                note_path.write_text(new_content, encoding="utf-8")
            else:
                logger.info("Creating note...")
                note_path.write_text(self._render_content(content), encoding="utf-8")
        except OSError as exc:
            raise ObsidianWriteError("Unable to write Obsidian note") from exc

        logger.info("Obsidian note updated successfully.")

    def _render_content(self, content: list[Any]) -> str:
        if not content:
            return ""
        return "\n".join(str(item) for item in content)

    def _join_content(self, existing_content: str, content: list[Any]) -> str:
        if not content:
            return existing_content

        rendered_content = self._render_content(content)
        if existing_content and rendered_content:
            return existing_content.rstrip("\n") + "\n\n" + rendered_content
        return existing_content + rendered_content
