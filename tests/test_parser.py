import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.exceptions.planner_exceptions import (
    InvalidPlannerJSONError,
    PlannerBlockNotFoundError,
    PlannerValidationError,
    UnsupportedPlannerVersionError,
)
from app.parser.parser import PlannerParser
from app.parser.schema import PlannerCommand


def test_parse_valid_planner_block() -> None:
    parser = PlannerParser()
    text = """
    Some human readable explanation...

    <!-- AI_PLANNER_START -->
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [],
        "tasks": [],
        "obsidian": {}
    }
    <!-- AI_PLANNER_END -->
    """

    command = parser.parse(text)

    assert isinstance(command, PlannerCommand)
    assert command == PlannerCommand(
        version=1,
        type="daily_plan",
        calendar=[],
        tasks=[],
        obsidian={},
    )


def test_parse_raises_when_start_marker_is_missing() -> None:
    parser = PlannerParser()
    text = """
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [],
        "tasks": [],
        "obsidian": {}
    }
    <!-- AI_PLANNER_END -->
    """

    with pytest.raises(PlannerBlockNotFoundError):
        parser.parse(text)


def test_parse_raises_when_end_marker_is_missing() -> None:
    parser = PlannerParser()
    text = """
    <!-- AI_PLANNER_START -->
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [],
        "tasks": [],
        "obsidian": {}
    }
    """

    with pytest.raises(PlannerBlockNotFoundError):
        parser.parse(text)


def test_parse_raises_for_malformed_json() -> None:
    parser = PlannerParser()
    text = """
    <!-- AI_PLANNER_START -->
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [],
        "tasks": [],
        "obsidian": {
    }
    <!-- AI_PLANNER_END -->
    """

    with pytest.raises(InvalidPlannerJSONError):
        parser.parse(text)


def test_parse_raises_for_unsupported_version() -> None:
    parser = PlannerParser()
    text = """
    <!-- AI_PLANNER_START -->
    {
        "version": 2,
        "type": "daily_plan",
        "calendar": [],
        "tasks": [],
        "obsidian": {}
    }
    <!-- AI_PLANNER_END -->
    """

    with pytest.raises(UnsupportedPlannerVersionError):
        parser.parse(text)


def test_parse_raises_for_missing_required_field() -> None:
    parser = PlannerParser()
    text = """
    <!-- AI_PLANNER_START -->
    {
        "version": 1,
        "type": "daily_plan",
        "calendar": [],
        "obsidian": {}
    }
    <!-- AI_PLANNER_END -->
    """

    with pytest.raises(PlannerValidationError):
        parser.parse(text)


def test_parse_raises_for_empty_planner_block() -> None:
    parser = PlannerParser()
    text = """
    <!-- AI_PLANNER_START -->

    <!-- AI_PLANNER_END -->
    """

    with pytest.raises(InvalidPlannerJSONError):
        parser.parse(text)
