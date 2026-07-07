"""Planner block parsing for PlannerOS."""

from __future__ import annotations

import json
import logging
import re
from json import JSONDecodeError
from typing import Any

from app.exceptions.planner_exceptions import (
    InvalidPlannerJSONError,
    PlannerBlockNotFoundError,
    PlannerValidationError,
    UnsupportedPlannerVersionError,
)
from app.parser.schema import PlannerCommand

LOGGER = logging.getLogger(__name__)

START_MARKER = "<!-- AI_PLANNER_START -->"
END_MARKER = "<!-- AI_PLANNER_END -->"
SUPPORTED_VERSION = 1
REQUIRED_FIELDS = ("version", "type", "calendar", "tasks", "obsidian")


class PlannerParser:
    """Parse and validate planner commands from ChatGPT responses."""

    def parse(self, text: str) -> PlannerCommand:
        """Extract a planner block from text and return a validated command."""
        json_text = self._extract_json_block(text)
        payload = self._load_json(json_text)
        return self._validate_payload(payload)

    def _extract_json_block(self, text: str) -> str:
        """Return the raw JSON content between planner markers."""
        if START_MARKER not in text or END_MARKER not in text:
            LOGGER.debug("Planner block markers missing from input text.")
            raise PlannerBlockNotFoundError("Planner block markers were not found.")

        pattern = rf"{re.escape(START_MARKER)}(.*?){re.escape(END_MARKER)}"
        match = re.search(pattern, text, re.DOTALL)

        if match is None:
            LOGGER.debug("Planner block content could not be extracted.")
            raise PlannerBlockNotFoundError("Planner block markers were not found.")

        json_text = match.group(1).strip()

        if not json_text:
            LOGGER.debug("Planner block was empty.")
            raise InvalidPlannerJSONError("Planner block is empty.")

        return json_text

    def _load_json(self, json_text: str) -> Any:
        """Decode JSON text from the planner block."""
        try:
            return json.loads(json_text)
        except JSONDecodeError as error:
            LOGGER.debug("Planner JSON could not be decoded: %s", error)
            raise InvalidPlannerJSONError("Planner block contains invalid JSON.") from error

    def _validate_payload(self, payload: Any) -> PlannerCommand:
        """Validate the decoded planner payload and build a command object."""
        if not isinstance(payload, dict):
            LOGGER.debug("Planner payload is not a JSON object: %s", type(payload).__name__)
            raise PlannerValidationError("Planner payload must be a JSON object.")

        self._validate_required_fields(payload)
        self._validate_version(payload["version"])
        self._validate_field_types(payload)

        return PlannerCommand(
            version=payload["version"],
            type=payload["type"],
            calendar=payload["calendar"],
            tasks=payload["tasks"],
            obsidian=payload["obsidian"],
        )

    def _validate_required_fields(self, payload: dict[str, Any]) -> None:
        """Ensure all required planner fields are present."""
        missing_fields = [field for field in REQUIRED_FIELDS if field not in payload]

        if missing_fields:
            LOGGER.debug("Planner payload missing fields: %s", ", ".join(missing_fields))
            raise PlannerValidationError(
                f"Planner payload is missing required fields: {', '.join(missing_fields)}."
            )

    def _validate_version(self, version: Any) -> None:
        """Ensure the planner protocol version is supported."""
        if version != SUPPORTED_VERSION:
            LOGGER.debug("Unsupported planner version received: %s", version)
            raise UnsupportedPlannerVersionError(
                f"Unsupported planner version: {version}."
            )

    def _validate_field_types(self, payload: dict[str, Any]) -> None:
        """Ensure planner fields match the MVP schema types."""
        if not isinstance(payload["type"], str):
            raise PlannerValidationError("Planner field 'type' must be a string.")

        if not isinstance(payload["calendar"], list):
            raise PlannerValidationError("Planner field 'calendar' must be a list.")

        if not isinstance(payload["tasks"], list):
            raise PlannerValidationError("Planner field 'tasks' must be a list.")

        if not isinstance(payload["obsidian"], dict):
            raise PlannerValidationError("Planner field 'obsidian' must be an object.")
