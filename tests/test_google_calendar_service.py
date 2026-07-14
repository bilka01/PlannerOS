import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.exceptions.planner_exceptions import (
    GoogleAuthenticationError,
    GoogleCalendarAPIError,
    MissingGoogleCredentialsError,
)
from app.integrations.google.calendar_service import GoogleCalendarService


class FakeCredentials:
    def __init__(
        self,
        *,
        valid: bool = True,
        expired: bool = False,
        refresh_token: str | None = None,
        token_json: str = '{"token":"value"}',
    ) -> None:
        self.valid = valid
        self.expired = expired
        self.refresh_token = refresh_token
        self.token_json = token_json
        self.refresh_calls: list[object] = []

    def refresh(self, request: object) -> None:
        self.refresh_calls.append(request)
        self.valid = True
        self.expired = False

    def to_json(self) -> str:
        return self.token_json


class FakeEventsResource:
    def __init__(self, response: dict) -> None:
        self.response = response
        self.insert_calls: list[tuple[str, dict]] = []

    def insert(self, *, calendarId: str, body: dict) -> "FakeEventsResource":
        self.insert_calls.append((calendarId, body))
        return self

    def execute(self) -> dict:
        return self.response


class FakeCalendarClient:
    def __init__(self, response: dict) -> None:
        self.events_resource = FakeEventsResource(response)

    def events(self) -> FakeEventsResource:
        return self.events_resource


def test_create_event_maps_fields_and_inserts_into_primary_calendar(monkeypatch) -> None:
    service = GoogleCalendarService()
    fake_client = FakeCalendarClient({"id": "abc123", "status": "confirmed"})
    monkeypatch.setattr(service, "_get_calendar_service", lambda: fake_client)

    result = service.create_event(
        {
            "title": "Doctor Appointment",
            "start": "2026-07-10T09:00",
            "end": "2026-07-10T10:00",
            "location": "Clinic",
            "description": "Annual checkup",
        }
    )

    assert result == {"id": "abc123", "status": "confirmed"}
    assert fake_client.events_resource.insert_calls == [
        (
            "primary",
            {
                "summary": "Doctor Appointment",
                "location": "Clinic",
                "description": "Annual checkup",
                "start": {
                    "dateTime": "2026-07-10T09:00",
                    "timeZone": "Europe/Bratislava",
                },
                "end": {
                    "dateTime": "2026-07-10T10:00",
                    "timeZone": "Europe/Bratislava",
                },
            },
        )
    ]


def test_get_credentials_reuses_valid_cached_credentials(monkeypatch, tmp_path: Path) -> None:
    token_path = tmp_path / "token.json"
    token_path.write_text("{}", encoding="utf-8")

    expected_credentials = FakeCredentials(valid=True)

    class FakeCredentialsClass:
        @staticmethod
        def from_authorized_user_file(path: str, scopes: list[str]) -> FakeCredentials:
            assert path == str(token_path)
            assert scopes
            return expected_credentials

    monkeypatch.setattr(
        "app.integrations.google.calendar_service.import_module",
        lambda name: SimpleNamespace(Credentials=FakeCredentialsClass)
        if name == "google.oauth2.credentials"
        else None,
    )

    service = GoogleCalendarService(
        client_secret_path=tmp_path / "client_secret.json",
        token_path=token_path,
    )

    credentials = service._get_credentials()

    assert credentials is expected_credentials


def test_get_credentials_refreshes_expired_cached_credentials(
    monkeypatch,
    tmp_path: Path,
) -> None:
    token_path = tmp_path / "token.json"
    token_path.write_text("{}", encoding="utf-8")
    refreshed_credentials = FakeCredentials(
        valid=False,
        expired=True,
        refresh_token="refresh-token",
    )

    class FakeCredentialsClass:
        @staticmethod
        def from_authorized_user_file(path: str, scopes: list[str]) -> FakeCredentials:
            assert path == str(token_path)
            assert scopes
            return refreshed_credentials

    def fake_import_module(name: str) -> object:
        if name == "google.oauth2.credentials":
            return SimpleNamespace(Credentials=FakeCredentialsClass)
        if name == "google.auth.transport.requests":
            return SimpleNamespace(Request=lambda: "request-object")
        raise AssertionError(f"Unexpected module import: {name}")

    monkeypatch.setattr(
        "app.integrations.google.calendar_service.import_module",
        fake_import_module,
    )

    service = GoogleCalendarService(
        client_secret_path=tmp_path / "client_secret.json",
        token_path=token_path,
    )

    credentials = service._get_credentials()

    assert credentials is refreshed_credentials
    assert refreshed_credentials.refresh_calls == ["request-object"]
    assert token_path.read_text(encoding="utf-8") == '{"token":"value"}'


def test_get_credentials_runs_oauth_flow_and_persists_token(
    monkeypatch,
    tmp_path: Path,
) -> None:
    client_secret_path = tmp_path / "client_secret.json"
    client_secret_path.write_text("{}", encoding="utf-8")
    token_path = tmp_path / "token.json"
    authenticated_credentials = FakeCredentials(valid=True, token_json='{"token":"new"}')

    class FakeInstalledAppFlow:
        @staticmethod
        def from_client_secrets_file(path: str, scopes: list[str]) -> object:
            assert path == str(client_secret_path)
            assert scopes
            return SimpleNamespace(
                run_local_server=lambda port, open_browser: authenticated_credentials
            )

    def fake_import_module(name: str) -> object:
        if name == "google_auth_oauthlib.flow":
            return SimpleNamespace(InstalledAppFlow=FakeInstalledAppFlow)
        raise AssertionError(f"Unexpected module import: {name}")

    monkeypatch.setattr(
        "app.integrations.google.calendar_service.import_module",
        fake_import_module,
    )

    service = GoogleCalendarService(
        client_secret_path=client_secret_path,
        token_path=token_path,
    )

    credentials = service._get_credentials()

    assert credentials is authenticated_credentials
    assert token_path.read_text(encoding="utf-8") == '{"token":"new"}'


def test_get_credentials_raises_for_missing_client_secret(tmp_path: Path) -> None:
    service = GoogleCalendarService(
        client_secret_path=tmp_path / "missing-client-secret.json",
        token_path=tmp_path / "token.json",
    )

    with pytest.raises(MissingGoogleCredentialsError):
        service._get_credentials()


def test_create_event_wraps_google_api_errors(monkeypatch) -> None:
    class FakeHttpError(Exception):
        pass

    class FailingEventsResource:
        def insert(self, *, calendarId: str, body: dict) -> "FailingEventsResource":
            return self

        def execute(self) -> dict:
            raise FakeHttpError("boom")

    class FailingCalendarClient:
        def events(self) -> FailingEventsResource:
            return FailingEventsResource()

    def fake_import_module(name: str) -> object:
        if name == "googleapiclient.errors":
            return SimpleNamespace(HttpError=FakeHttpError)
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(
        "app.integrations.google.calendar_service.import_module",
        fake_import_module,
    )

    service = GoogleCalendarService()
    monkeypatch.setattr(service, "_get_calendar_service", lambda: FailingCalendarClient())

    with pytest.raises(GoogleCalendarAPIError):
        service.create_event({"title": "Doctor Appointment"})


def test_get_credentials_wraps_oauth_failures(monkeypatch, tmp_path: Path) -> None:
    client_secret_path = tmp_path / "client_secret.json"
    client_secret_path.write_text("{}", encoding="utf-8")

    class FakeInstalledAppFlow:
        @staticmethod
        def from_client_secrets_file(path: str, scopes: list[str]) -> object:
            return SimpleNamespace(
                run_local_server=lambda port, open_browser: (_ for _ in ()).throw(
                    RuntimeError("oauth failed")
                )
            )

    monkeypatch.setattr(
        "app.integrations.google.calendar_service.import_module",
        lambda name: SimpleNamespace(InstalledAppFlow=FakeInstalledAppFlow)
        if name == "google_auth_oauthlib.flow"
        else None,
    )

    service = GoogleCalendarService(
        client_secret_path=client_secret_path,
        token_path=tmp_path / "token.json",
    )

    with pytest.raises(GoogleAuthenticationError):
        service._get_credentials()
