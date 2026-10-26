import os
from uuid import UUID

import pytest

from lumos.common.helpers import authenticate, check_current_apps, get_statuses
from lumos.common.models import (
    AccessRequest,
    App,
    Permission,
    SupportRequestStatus,
    User,
)


class TestAuthenticateCheckOnly:
    """LUMOS_CHECK_ONLY makes @authenticate a non-interactive check instead of
    an implicit login trigger. See the whoami --check flag in cli.py."""

    def teardown_method(self):
        os.environ.pop("API_KEY", None)
        os.environ.pop("SCOPE", None)

    def test_exits_nonzero_without_prompting_when_no_credential(self, monkeypatch, tmp_path):
        monkeypatch.setenv("LUMOS_CHECK_ONLY", "1")
        monkeypatch.delenv("API_KEY", raising=False)
        monkeypatch.setattr("lumos.common.helpers.key_file_path", lambda: tmp_path / "missing-key")

        calls = []

        @authenticate
        def fake_command():
            calls.append("ran")

        with pytest.raises(SystemExit) as exc_info:
            fake_command()

        assert exc_info.value.code == 1
        assert calls == []  # the wrapped command must never run

    def test_proceeds_when_key_file_exists(self, monkeypatch, tmp_path):
        key_file = tmp_path / "key"
        key_file.write_text("user:some-token")
        monkeypatch.setenv("LUMOS_CHECK_ONLY", "1")
        monkeypatch.delenv("API_KEY", raising=False)
        monkeypatch.setattr("lumos.common.helpers.key_file_path", lambda: key_file)
        # read_key() (called after the existence check passes) resolves
        # key_file_path() via its own module reference, not helpers', so it
        # must be patched too or this reads the real ~/.lumos on the machine.
        monkeypatch.setattr("lumos.common.keyhelpers.key_file_path", lambda: key_file)

        @authenticate
        def fake_command():
            return "ran"

        assert fake_command() == "ran"
        assert os.environ.get("API_KEY") == "some-token"

    def test_proceeds_when_api_key_env_already_set(self, monkeypatch, tmp_path):
        monkeypatch.setenv("LUMOS_CHECK_ONLY", "1")
        monkeypatch.setenv("API_KEY", "env-token")
        monkeypatch.setattr("lumos.common.helpers.key_file_path", lambda: tmp_path / "missing-key")

        @authenticate
        def fake_command():
            return "ran"

        assert fake_command() == "ran"


def test_get_statuses():
    assert get_statuses([], False, False) is None
    assert get_statuses(None, False, False) is None


def test_get_statuses_just_pending():
    assert get_statuses([SupportRequestStatus.PENDING], False, False) == {SupportRequestStatus.PENDING}
    assert get_statuses([SupportRequestStatus.PENDING], True, False) == set(SupportRequestStatus.PENDING_STATUSES)
    assert get_statuses([], True, False) == set(SupportRequestStatus.PENDING_STATUSES)


def test_get_statusees_pending_and_past():
    not_pending = set(SupportRequestStatus.ALL_STATUSES).difference(set(SupportRequestStatus.PENDING_STATUSES))
    not_pending.add(SupportRequestStatus.PENDING)
    assert get_statuses([SupportRequestStatus.PENDING], False, True) == not_pending
    assert get_statuses([SupportRequestStatus.PENDING], True, True) == set(SupportRequestStatus.ALL_STATUSES)

    pending_and_completed = set(SupportRequestStatus.PENDING_STATUSES)
    pending_and_completed.add(SupportRequestStatus.COMPLETED)
    assert get_statuses([SupportRequestStatus.COMPLETED], True, False) == pending_and_completed


def test_get_statuses_all_statuses():
    assert get_statuses([], True, True) == set(SupportRequestStatus.ALL_STATUSES)


def test_check_current_apps():
    user = User(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        given_name="John",
        family_name="Doe",
        email="foo@foo.com",
    )
    app1 = App(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        name="app",
        user_friendly_label="App 1",
        app_class_id="foo",
        instance_id="bar",
    )
    app2 = App(
        id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        name="app",
        user_friendly_label="App 2",
        app_class_id="foo",
        instance_id="bar",
    )
    permission1 = Permission(
        id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        label="permission",
        app_id=str(app1.id),
        app_class_id="foo",
    )
    permission2 = Permission(
        id=UUID("123e4567-e89b-12d3-a456-426614174002"),
        label="permission",
        app_id=str(app1.id),
        app_class_id="foo",
    )
    permission3 = Permission(
        id=UUID("123e4567-e89b-12d3-a456-426614174003"),
        label="permission",
        app_id=str(app1.id),
        app_class_id="foo",
    )
    access_request1 = AccessRequest(
        id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        app_id=app1.id,
        requestable_permissions=[permission1, permission2],
        requested_at="2021-01-01",
        supporter_user=user,
        requester_user=user,
        target_user=user,
        app_name="app",
        status="PENDING",
        expires_at=None,
    )
    access_request2 = AccessRequest(
        id=UUID("123e4567-e89b-12d3-a456-426614174002"),
        app_id=app2.id,
        requestable_permissions=[],
        requested_at="2021-01-01",
        supporter_user=user,
        requester_user=user,
        target_user=user,
        app_name="app",
        status="PENDING",
        expires_at=None,
    )
    assert check_current_apps([access_request1], app1, [permission1]) == (
        access_request1,
        "There's already a request for this app and permission",
    )
    assert check_current_apps([access_request1], app1, [permission2]) == (
        access_request1,
        "There's already a request for this app and permission",
    )
    assert check_current_apps([access_request1], app1, [permission3]) == (None, None)
    assert check_current_apps([access_request1], app2, []) == (None, None)
    assert check_current_apps([access_request2], app2, []) == (
        access_request2,
        "There's already a request for this app",
    )
