"""Custom exceptions for PlannerOS parsing and validation."""


class PlannerError(Exception):
    """Base exception for planner-related errors."""


class PlannerBlockNotFoundError(PlannerError):
    """Raised when the planner block markers cannot be found."""


class InvalidPlannerJSONError(PlannerError):
    """Raised when the planner block does not contain valid JSON."""


class UnsupportedPlannerVersionError(PlannerError):
    """Raised when the planner block uses an unsupported protocol version."""


class PlannerValidationError(PlannerError):
    """Raised when required planner fields are missing or invalid."""
