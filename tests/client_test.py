"""
Tests for BaseClient._send_request's 401 handling, in particular the
LUMOS_CHECK_ONLY escape hatch (see whoami --check in cli.py). Without it, a
present-but-expired/invalid credential makes any authenticated command
silently kick off the full interactive OAuth device flow (open a browser,
block polling for approval) with no way to opt out.
"""

import os
from unittest.mock import patch

import pytest
import requests

from lumos.common.client import ApiClient


@pytest.fixture(autouse=True)
def _clean_auth_env():
    for var in ("LUMOS_CHECK_ONLY", "API_KEY", "SCOPE"):
        os.environ.pop(var, None)
    yield
    for var in ("LUMOS_CHECK_ONLY", "API_KEY", "SCOPE"):
        os.environ.pop(var, None)


def _unauthorized_response() -> requests.Response:
    response = requests.Response()
    response.status_code = 401
    return response


def test_401_with_check_only_exits_without_triggering_reauth(monkeypatch):
    """This is the fix: previously a 401 with a SCOPE set unconditionally
    called AuthClient().authenticate() (the interactive OAuth flow) with no
    way to suppress it."""
    monkeypatch.setenv("LUMOS_CHECK_ONLY", "1")
    monkeypatch.setenv("API_KEY", "stale-token")
    monkeypatch.setenv("SCOPE", "user")

    with (
        patch("lumos.common.client.requests.request", return_value=_unauthorized_response()) as mock_request,
        patch("lumos.common.client.AuthClient.authenticate") as mock_authenticate,
        pytest.raises(SystemExit) as exc_info,
    ):
        ApiClient().get("users/current")

    assert exc_info.value.code == 1
    mock_authenticate.assert_not_called()
    mock_request.assert_called_once()


def test_401_without_check_only_still_auto_reauths(monkeypatch):
    """Regression guard: pre-existing behavior (no LUMOS_CHECK_ONLY set) must
    be unchanged, since callers relying on the current auto-relogin-on-401
    convenience shouldn't be broken by this change. The retry loop calls
    AuthClient().authenticate() on every 401 until retry > 1, then gives up;
    with every attempt still coming back 401 that means two auto-relogin
    attempts before it exits."""
    monkeypatch.setenv("API_KEY", "stale-token")
    monkeypatch.setenv("SCOPE", "user")

    with (
        patch(
            "lumos.common.client.requests.request",
            side_effect=lambda *a, **k: _unauthorized_response(),
        ),
        patch("lumos.common.client.AuthClient.authenticate") as mock_authenticate,
        pytest.raises(SystemExit),
    ):
        ApiClient().get("users/current")

    assert mock_authenticate.call_count == 2
