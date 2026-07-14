"""Custom exceptions for PlannerOS parsing, validation, and integrations."""


class PlannerError(Exception):
    """Base exception for planner-related errors."""


class ClipboardError(PlannerError):
    """Raised when the clipboard contents cannot be read."""


class PlannerBlockNotFoundError(PlannerError):
    """Raised when the planner block markers cannot be found."""


class InvalidPlannerJSONError(PlannerError):
    """Raised when the planner block does not contain valid JSON."""


class UnsupportedPlannerVersionError(PlannerError):
    """Raised when the planner block uses an unsupported protocol version."""


class PlannerValidationError(PlannerError):
    """Raised when required planner fields are missing or invalid."""


class CalendarIntegrationError(PlannerError):
    """Base exception for calendar integration failures."""


class MissingGoogleCredentialsError(CalendarIntegrationError):
    """Raised when Google OAuth client credentials are not available."""


class GoogleAuthenticationError(CalendarIntegrationError):
    """Raised when Google Calendar authentication fails."""


class GoogleCalendarAPIError(CalendarIntegrationError):
    """Raised when Google Calendar API operations fail."""


class ObsidianIntegrationError(PlannerError):
    """Base exception for Obsidian integration failures."""


class ObsidianVaultNotFoundError(ObsidianIntegrationError):
    """Raised when the configured Obsidian vault does not exist."""


class ObsidianWriteError(ObsidianIntegrationError):
    """Raised when an Obsidian note cannot be created or updated."""
