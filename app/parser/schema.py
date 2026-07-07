"""Schema definitions for PlannerOS parser output."""

from dataclasses import dataclass


@dataclass(slots=True)
class PlannerCommand:
    """Validated planner command extracted from a ChatGPT response."""

    version: int
    type: str
    calendar: list
    tasks: list
    obsidian: dict
