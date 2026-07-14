"""Google Calendar service for PlannerOS calendar event creation."""

from __future__ import annotations

import os
from importlib import import_module
from pathlib import Path
from typing import Any

from app.exceptions.planner_exceptions import (
    GoogleAuthenticationError,
    GoogleCalendarAPIError,
    MissingGoogleCredentialsError,
)
from app.utils.logging import get_logger

logger = get_logger("planneros.integrations.google.calendar")

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CLIENT_SECRET_ENV = "PLANNEROS_GOOGLE_CLIENT_SECRET_FILE"
TOKEN_FILE_ENV = "PLANNEROS_GOOGLE_TOKEN_FILE"
DEFAULT_TIME_ZONE = "Europe/Bratislava"


class GoogleCalendarService:
    """Create Google Calendar events using the Desktop OAuth flow."""

    def __init__(
        self,
        client_secret_path: Path | None = None,
        token_path: Path | None = None,
    ) -> None:
        credentials_dir = self._get_credentials_dir()
        self._client_secret_path = (
            client_secret_path
            or self._path_from_env(CLIENT_SECRET_ENV)
            or credentials_dir / "client_secret.json"
        )
        self._token_path = (
            token_path
            or self._path_from_env(TOKEN_FILE_ENV)
            or credentials_dir / "token.json"
        )
        self._calendar_service: Any | None = None

    def create_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Create a single event in the user's primary Google Calendar."""
        service = self._get_calendar_service()
        payload = self._build_event_payload(event)

        try:
            return (
                service.events()
                .insert(calendarId="primary", body=payload)
                .execute()
            )
        except Exception as error:
            logger.exception("Google Calendar API request failed.")
            raise GoogleCalendarAPIError(
                "Failed to create Google Calendar event."
            ) from error

    def _get_calendar_service(self) -> Any:
        """Build and cache the Google Calendar API client."""
        if self._calendar_service is None:
            credentials = self._get_credentials()
            build = import_module("googleapiclient.discovery").build

            try:
                self._calendar_service = build(
                    "calendar",
                    "v3",
                    credentials=credentials,
                    cache_discovery=False,
                )
            except Exception as error:
                logger.exception("Failed to initialize Google Calendar API client.")
                raise GoogleCalendarAPIError(
                    "Failed to initialize Google Calendar API client."
                ) from error

        return self._calendar_service

    def _get_credentials(self) -> Any:
        """Load, refresh, or create Google OAuth credentials."""
        credentials = self._load_cached_credentials()

        if credentials is not None and getattr(credentials, "valid", False):
            logger.info("Reusing existing Google Calendar credentials.")
            return credentials

        if (
            credentials is not None
            and getattr(credentials, "expired", False)
            and getattr(credentials, "refresh_token", None)
        ):
            logger.info("Refreshing Google Calendar credentials...")
            request = import_module("google.auth.transport.requests").Request

            try:
                credentials.refresh(request())
            except Exception as error:
                logger.exception("Failed to refresh Google Calendar credentials.")
                raise GoogleAuthenticationError(
                    "Failed to refresh Google Calendar credentials."
                ) from error

            self._write_token(credentials)
            logger.info("Authentication successful.")
            return credentials

        if not self._client_secret_path.exists():
            raise MissingGoogleCredentialsError(
                "Google OAuth client credentials were not found. "
                f"Expected file: {self._client_secret_path}"
            )

        logger.info("Authenticating with Google Calendar...")
        flow = import_module("google_auth_oauthlib.flow").InstalledAppFlow

        try:
            app_flow = flow.from_client_secrets_file(
                str(self._client_secret_path),
                SCOPES,
            )
            credentials = app_flow.run_local_server(port=0, open_browser=True)
        except Exception as error:
            logger.exception("Google Calendar authentication failed.")
            raise GoogleAuthenticationError(
                "Failed to authenticate with Google Calendar."
            ) from error

        self._write_token(credentials)
        logger.info("Authentication successful.")
        return credentials

    def _load_cached_credentials(self) -> Any | None:
        """Return cached Google OAuth credentials, if available."""
        if not self._token_path.exists():
            return None

        credentials_class = import_module("google.oauth2.credentials").Credentials

        try:
            return credentials_class.from_authorized_user_file(
                str(self._token_path),
                SCOPES,
            )
        except Exception as error:
            logger.exception("Failed to load cached Google Calendar credentials.")
            raise GoogleAuthenticationError(
                "Failed to load cached Google Calendar credentials."
            ) from error

    def _write_token(self, credentials: Any) -> None:
        """Persist Google OAuth credentials for reuse on future runs."""
        self._token_path.parent.mkdir(parents=True, exist_ok=True)
        self._token_path.write_text(credentials.to_json(), encoding="utf-8")

    def _build_event_payload(self, event: dict[str, Any]) -> dict[str, Any]:
        """Map PlannerOS calendar event data to the Google Calendar API format."""
        return {
            "summary": event.get("title"),
            "location": event.get("location"),
            "description": event.get("description"),
            "start": {
                "dateTime": event.get("start"),
                "timeZone": DEFAULT_TIME_ZONE,
            },
            "end": {
                "dateTime": event.get("end"),
                "timeZone": DEFAULT_TIME_ZONE,
            },
        }

    def _get_credentials_dir(self) -> Path:
        """Return the local directory used for Google OAuth files."""
        return Path.home() / ".planneros" / "google"

    def _path_from_env(self, env_name: str) -> Path | None:
        """Return a configured path from the environment, if set."""
        value = os.getenv(env_name)
        if not value:
            return None

        return Path(value).expanduser()
