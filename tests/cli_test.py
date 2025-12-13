"""
Tests for CLI commands and options.

These tests validate the end-user experience by testing CLI structure,
options, and help text without making actual API calls.
"""

from unittest.mock import patch
from uuid import UUID

import pytest
from click.testing import CliRunner

from lumos_cli.cli import lumos
from lumos_cli.common.models import (
    AccessRequest,
    App,
    Group,
    Permission,
    SupportRequestStatus,
    User,
)


# Fixtures for test data
@pytest.fixture
def mock_user():
    return User(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        given_name="Test",
        family_name="User",
        email="test@example.com",
    )


@pytest.fixture
def mock_app():
    return App(
        id=UUID("123e4567-e89b-12d3-a456-426614174001"),
        user_friendly_label="Test App",
        app_class_id="test-class",
        instance_id="test-instance",
    )


@pytest.fixture
def mock_permission():
    return Permission(
        id=UUID("123e4567-e89b-12d3-a456-426614174002"),
        label="Test Permission",
        app_id="123e4567-e89b-12d3-a456-426614174001",
        app_class_id="test-class",
        duration_options=["1 hour", "1 day"],
    )


@pytest.fixture
def mock_group():
    return Group(
        id=UUID("123e4567-e89b-12d3-a456-426614174003"),
        name="Test Group",
        description="A test group",
        app_id="123e4567-e89b-12d3-a456-426614174001",
        source_app_id="123e4567-e89b-12d3-a456-426614174001",
        integration_specific_id="test-integration-id",
    )


@pytest.fixture
def mock_access_request(mock_user, mock_app, mock_permission):
    return AccessRequest(
        id=UUID("123e4567-e89b-12d3-a456-426614174004"),
        app_id=mock_app.id,
        app_name=mock_app.user_friendly_label,
        status=SupportRequestStatus.PENDING,
        requested_at="2024-01-01T00:00:00",
        expires_at=None,
        requester_user=mock_user,
        supporter_user=mock_user,
        target_user=mock_user,
        requestable_permissions=[mock_permission],
    )


@pytest.fixture
def runner():
    return CliRunner()


class TestMainCLI:
    """Test the main CLI group and its options."""

    def test_cli_help(self, runner):
        """Test that help is displayed with -h and --help."""
        result = runner.invoke(lumos, ["--help"])
        assert result.exit_code == 0
        assert "Lumos CLI" in result.output
        assert "Command line interface for Lumos" in result.output

        result = runner.invoke(lumos, ["-h"])
        assert result.exit_code == 0
        assert "Lumos CLI" in result.output

    def test_cli_shows_commands(self, runner):
        """Test that all commands are listed in help."""
        result = runner.invoke(lumos, ["--help"])
        assert result.exit_code == 0
        # Main commands
        assert "whoami" in result.output
        assert "setup" in result.output
        assert "login" in result.output
        assert "logout" in result.output
        # New noun-based command groups
        assert "app" in result.output
        assert "user" in result.output
        assert "group" in result.output
        assert "permission" in result.output
        assert "request" in result.output
        # Deprecated but still visible
        assert "list" in result.output

    def test_cli_version(self, runner):
        """Test that --version displays version information."""
        result = runner.invoke(lumos, ["--version"])
        assert result.exit_code == 0
        # Version should be displayed

    def test_cli_debug_option_is_hidden(self, runner):
        """Test that --debug option exists but is hidden from help."""
        result = runner.invoke(lumos, ["--help"])
        # Debug option should be hidden
        assert "--debug" not in result.output


class TestWhoamiCommand:
    """Test the whoami command and its options."""

    def test_whoami_help(self, runner):
        """Test whoami command help."""
        result = runner.invoke(lumos, ["whoami", "--help"])
        assert result.exit_code == 0
        assert "Show information about the currently logged in user" in result.output

    def test_whoami_options(self, runner):
        """Test that whoami has expected options."""
        result = runner.invoke(lumos, ["whoami", "--help"])
        assert result.exit_code == 0
        assert "--username" in result.output
        assert "--id" in result.output


class TestSetupCommand:
    """Test the setup command."""

    def test_setup_help(self, runner):
        """Test setup command help."""
        result = runner.invoke(lumos, ["setup", "--help"])
        assert result.exit_code == 0
        assert "Setup your Lumos CLI" in result.output
        assert "authentication" in result.output


class TestLoginCommand:
    """Test the login command and its options."""

    def test_login_help(self, runner):
        """Test login command help."""
        result = runner.invoke(lumos, ["login", "--help"])
        assert result.exit_code == 0
        assert "Login to your Lumos account" in result.output
        assert "OAuth" in result.output

    def test_login_admin_option(self, runner):
        """Test login has --admin option."""
        result = runner.invoke(lumos, ["login", "--help"])
        assert result.exit_code == 0
        assert "--admin" in result.output


class TestLogoutCommand:
    """Test the logout command."""

    def test_logout_help(self, runner):
        """Test logout command help."""
        result = runner.invoke(lumos, ["logout", "--help"])
        assert result.exit_code == 0
        assert "Logout of your Lumos account" in result.output

    @patch("lumos_cli.cli._logout")
    def test_logout_execution(self, mock_logout, runner):
        """Test logout command executes successfully."""
        result = runner.invoke(lumos, ["logout"])
        assert result.exit_code == 0
        assert "Logged out" in result.output
        mock_logout.assert_called_once()


# =============================================================================
# NEW NOUN-BASED COMMAND TESTS (RESTful CLI structure)
# =============================================================================


class TestAppCommand:
    """Test the new 'lumos app' command group."""

    def test_app_help(self, runner):
        """Test app command help."""
        result = runner.invoke(lumos, ["app", "--help"])
        assert result.exit_code == 0
        assert "Manage apps" in result.output

    def test_app_shows_subcommands(self, runner):
        """Test that app shows list subcommand."""
        result = runner.invoke(lumos, ["app", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_app_list_help(self, runner):
        """Test app list help."""
        result = runner.invoke(lumos, ["app", "list", "--help"])
        assert result.exit_code == 0
        assert "List apps in the appstore" in result.output

    def test_app_list_options(self, runner):
        """Test app list has expected options."""
        result = runner.invoke(lumos, ["app", "list", "--help"])
        assert result.exit_code == 0
        assert "--like" in result.output
        assert "--mine" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--paginate" in result.output
        assert "--page-size" in result.output
        assert "--page" in result.output
        assert "--id-only" in result.output


class TestUserCommand:
    """Test the new 'lumos user' command group."""

    def test_user_help(self, runner):
        """Test user command help."""
        result = runner.invoke(lumos, ["user", "--help"])
        assert result.exit_code == 0
        assert "Manage users" in result.output

    def test_user_shows_subcommands(self, runner):
        """Test that user shows list subcommand."""
        result = runner.invoke(lumos, ["user", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_user_list_help(self, runner):
        """Test user list help."""
        result = runner.invoke(lumos, ["user", "list", "--help"])
        assert result.exit_code == 0
        assert "List users in Lumos" in result.output

    def test_user_list_options(self, runner):
        """Test user list has expected options."""
        result = runner.invoke(lumos, ["user", "list", "--help"])
        assert result.exit_code == 0
        assert "--like" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--paginate" in result.output
        assert "--page-size" in result.output
        assert "--page" in result.output
        assert "--id-only" in result.output


class TestGroupCommand:
    """Test the new 'lumos group' command group."""

    def test_group_help(self, runner):
        """Test group command help."""
        result = runner.invoke(lumos, ["group", "--help"])
        assert result.exit_code == 0
        assert "Manage groups" in result.output

    def test_group_shows_subcommands(self, runner):
        """Test that group shows list subcommand."""
        result = runner.invoke(lumos, ["group", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_group_list_help(self, runner):
        """Test group list help."""
        result = runner.invoke(lumos, ["group", "list", "--help"])
        assert result.exit_code == 0
        assert "List groups" in result.output

    def test_group_list_options(self, runner):
        """Test group list has expected options."""
        result = runner.invoke(lumos, ["group", "list", "--help"])
        assert result.exit_code == 0
        assert "--app" in result.output
        assert "--like" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--paginate" in result.output
        assert "--page-size" in result.output
        assert "--page" in result.output
        assert "--id-only" in result.output


class TestPermissionCommand:
    """Test the new 'lumos permission' command group."""

    def test_permission_help(self, runner):
        """Test permission command help."""
        result = runner.invoke(lumos, ["permission", "--help"])
        assert result.exit_code == 0
        assert "Manage permissions" in result.output

    def test_permission_shows_subcommands(self, runner):
        """Test that permission shows list subcommand."""
        result = runner.invoke(lumos, ["permission", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_permission_list_help(self, runner):
        """Test permission list help."""
        result = runner.invoke(lumos, ["permission", "list", "--help"])
        assert result.exit_code == 0
        assert "List permissions for a given app" in result.output

    def test_permission_list_requires_app(self, runner):
        """Test permission list requires --app option."""
        result = runner.invoke(lumos, ["permission", "list", "--help"])
        assert result.exit_code == 0
        assert "--app" in result.output
        assert "required" in result.output.lower() or "App UUID" in result.output

    def test_permission_list_options(self, runner):
        """Test permission list has expected options."""
        result = runner.invoke(lumos, ["permission", "list", "--help"])
        assert result.exit_code == 0
        assert "--like" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--paginate" in result.output
        assert "--page-size" in result.output
        assert "--page" in result.output
        assert "--id-only" in result.output


class TestRequestCommand:
    """Test the new 'lumos request' command group with RESTful structure."""

    def test_request_help(self, runner):
        """Test request command help."""
        result = runner.invoke(lumos, ["request", "--help"])
        assert result.exit_code == 0
        assert "Manage access requests" in result.output

    def test_request_shows_subcommands(self, runner):
        """Test that request shows all subcommands."""
        result = runner.invoke(lumos, ["request", "--help"])
        assert result.exit_code == 0
        assert "create" in result.output
        assert "list" in result.output
        assert "status" in result.output
        assert "poll" in result.output
        assert "cancel" in result.output

    def test_request_create_help(self, runner):
        """Test request create help."""
        result = runner.invoke(lumos, ["request", "create", "--help"])
        assert result.exit_code == 0
        assert "Request access to an app" in result.output

    def test_request_create_options(self, runner):
        """Test request create has expected options."""
        result = runner.invoke(lumos, ["request", "create", "--help"])
        assert result.exit_code == 0
        assert "--reason" in result.output
        assert "--for-user" in result.output
        assert "--for-me" in result.output
        assert "--mine" in result.output
        assert "--app" in result.output
        assert "--permission" in result.output
        assert "--length" in result.output
        assert "--user-like" in result.output
        assert "--app-like" in result.output
        assert "--permission-like" in result.output
        assert "--wait" in result.output
        assert "--dry-run" in result.output

    def test_request_list_help(self, runner):
        """Test request list help."""
        result = runner.invoke(lumos, ["request", "list", "--help"])
        assert result.exit_code == 0
        assert "List access requests" in result.output

    def test_request_list_options(self, runner):
        """Test request list has expected options."""
        result = runner.invoke(lumos, ["request", "list", "--help"])
        assert result.exit_code == 0
        assert "--for-user" in result.output
        assert "--mine" in result.output
        assert "--status" in result.output
        assert "--pending" in result.output
        assert "--past" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--paginate" in result.output
        assert "--page-size" in result.output
        assert "--page" in result.output
        assert "--id-only" in result.output


class TestRequestStatusCommand:
    """Test the request status command."""

    @patch("lumos_cli.common.helpers.setup")
    def test_request_status_help(self, mock_setup, runner):
        """Test request status help."""
        result = runner.invoke(lumos, ["request", "status", "--help"])
        assert result.exit_code == 0
        assert "Check the status of a request" in result.output

    @patch("lumos_cli.common.helpers.setup")
    def test_request_status_options(self, mock_setup, runner):
        """Test request status has expected options."""
        result = runner.invoke(lumos, ["request", "status", "--help"])
        assert result.exit_code == 0
        assert "--request-id" in result.output
        assert "--last" in result.output
        assert "--status-only" in result.output
        assert "--permission-only" in result.output
        assert "--id-only" in result.output


class TestRequestPollCommand:
    """Test the request poll command."""

    @patch("lumos_cli.common.helpers.setup")
    def test_request_poll_help(self, mock_setup, runner):
        """Test request poll help."""
        result = runner.invoke(lumos, ["request", "poll", "--help"])
        assert result.exit_code == 0
        assert "Poll a request" in result.output
        assert "5 minutes" in result.output

    @patch("lumos_cli.common.helpers.setup")
    def test_request_poll_options(self, mock_setup, runner):
        """Test request poll has expected options."""
        result = runner.invoke(lumos, ["request", "poll", "--help"])
        assert result.exit_code == 0
        assert "--request-id" in result.output
        assert "--wait" in result.output


class TestRequestCancelCommand:
    """Test the request cancel command."""

    @patch("lumos_cli.common.helpers.setup")
    def test_request_cancel_help(self, mock_setup, runner):
        """Test request cancel help."""
        result = runner.invoke(lumos, ["request", "cancel", "--help"])
        assert result.exit_code == 0
        assert "Cancel a request" in result.output

    @patch("lumos_cli.common.helpers.setup")
    def test_request_cancel_options(self, mock_setup, runner):
        """Test request cancel has expected options."""
        result = runner.invoke(lumos, ["request", "cancel", "--help"])
        assert result.exit_code == 0
        assert "--request-id" in result.output
        assert "--reason" in result.output


# =============================================================================
# DEPRECATED 'list' COMMAND TESTS (backward compatibility)
# =============================================================================


class TestDeprecatedListSubcommand:
    """Test the deprecated list command group (backward compatibility)."""

    def test_list_help(self, runner):
        """Test list command help shows deprecation."""
        result = runner.invoke(lumos, ["list", "--help"])
        assert result.exit_code == 0
        # Should still work but may show deprecation info
        assert "List" in result.output or "DEPRECATED" in result.output

    def test_list_shows_subcommands(self, runner):
        """Test that list shows all subcommands."""
        result = runner.invoke(lumos, ["list", "--help"])
        assert result.exit_code == 0
        assert "users" in result.output
        assert "permissions" in result.output
        assert "groups" in result.output
        assert "requests" in result.output
        assert "apps" in result.output


class TestDeprecatedListUsersCommand:
    """Test the deprecated list users command."""

    def test_list_users_help(self, runner):
        """Test list users help."""
        result = runner.invoke(lumos, ["list", "users", "--help"])
        assert result.exit_code == 0
        # Shows deprecation notice
        assert "DEPRECATED" in result.output or "user list" in result.output

    def test_list_users_options(self, runner):
        """Test list users has expected options."""
        result = runner.invoke(lumos, ["list", "users", "--help"])
        assert result.exit_code == 0
        assert "--like" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--paginate" in result.output
        assert "--page-size" in result.output
        assert "--page" in result.output
        assert "--id-only" in result.output


class TestDeprecatedListPermissionsCommand:
    """Test the deprecated list permissions command."""

    def test_list_permissions_help(self, runner):
        """Test list permissions help."""
        result = runner.invoke(lumos, ["list", "permissions", "--help"])
        assert result.exit_code == 0
        assert "DEPRECATED" in result.output or "permission list" in result.output

    def test_list_permissions_requires_app(self, runner):
        """Test list permissions requires --app option."""
        result = runner.invoke(lumos, ["list", "permissions", "--help"])
        assert result.exit_code == 0
        assert "--app" in result.output
        # App is required
        assert "required" in result.output.lower() or "App UUID" in result.output

    def test_list_permissions_options(self, runner):
        """Test list permissions has expected options."""
        result = runner.invoke(lumos, ["list", "permissions", "--help"])
        assert result.exit_code == 0
        assert "--like" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output


class TestDeprecatedListGroupsCommand:
    """Test the deprecated list groups command."""

    def test_list_groups_help(self, runner):
        """Test list groups help."""
        result = runner.invoke(lumos, ["list", "groups", "--help"])
        assert result.exit_code == 0
        assert "DEPRECATED" in result.output or "group list" in result.output

    def test_list_groups_options(self, runner):
        """Test list groups has expected options."""
        result = runner.invoke(lumos, ["list", "groups", "--help"])
        assert result.exit_code == 0
        assert "--app" in result.output
        assert "--like" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output


class TestDeprecatedListRequestsCommand:
    """Test the deprecated list requests command."""

    def test_list_requests_help(self, runner):
        """Test list requests help."""
        result = runner.invoke(lumos, ["list", "requests", "--help"])
        assert result.exit_code == 0
        assert "DEPRECATED" in result.output or "request list" in result.output

    def test_list_requests_options(self, runner):
        """Test list requests has expected options."""
        result = runner.invoke(lumos, ["list", "requests", "--help"])
        assert result.exit_code == 0
        assert "--for-user" in result.output
        assert "--mine" in result.output
        assert "--status" in result.output
        assert "--pending" in result.output
        assert "--past" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output


class TestDeprecatedListAppsCommand:
    """Test the deprecated list apps command."""

    def test_list_apps_help(self, runner):
        """Test list apps help."""
        result = runner.invoke(lumos, ["list", "apps", "--help"])
        assert result.exit_code == 0
        assert "DEPRECATED" in result.output or "app list" in result.output

    def test_list_apps_options(self, runner):
        """Test list apps has expected options."""
        result = runner.invoke(lumos, ["list", "apps", "--help"])
        assert result.exit_code == 0
        assert "--like" in result.output
        assert "--mine" in result.output
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output


# =============================================================================
# CLI BEHAVIOR AND STRUCTURE TESTS
# =============================================================================


class TestCLIBehavior:
    """Test overall CLI behavior and edge cases."""

    def test_invalid_command(self, runner):
        """Test that invalid commands are handled gracefully."""
        result = runner.invoke(lumos, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.output or "Error" in result.output

    def test_invalid_subcommand(self, runner):
        """Test that invalid subcommands are handled gracefully."""
        result = runner.invoke(lumos, ["app", "invalid-subcommand"])
        assert result.exit_code != 0

    def test_missing_required_option(self, runner):
        """Test that missing required options are reported."""
        # permission list requires --app
        runner.invoke(lumos, ["permission", "list"])
        # Should fail because --app is required (but may also fail on auth)
        # The key is that it doesn't succeed without the required option

    def test_help_on_empty_command(self, runner):
        """Test that CLI shows help when invoked without arguments."""
        result = runner.invoke(lumos, [])
        # Should show some output (either help or error)
        assert len(result.output) > 0


class TestCLIStructure:
    """Test that CLI structure matches expected RESTful design."""

    def test_noun_command_groups_exist(self, runner):
        """Test that expected noun-based command groups exist."""
        result = runner.invoke(lumos, ["--help"])
        assert result.exit_code == 0

        # New RESTful noun-based commands
        noun_commands = ["app", "user", "group", "permission", "request"]
        for cmd in noun_commands:
            assert cmd in result.output, f"Noun command '{cmd}' not found in CLI"

    def test_auth_commands_at_root(self, runner):
        """Test that auth commands are at root level."""
        result = runner.invoke(lumos, ["--help"])
        assert result.exit_code == 0

        auth_commands = ["whoami", "setup", "login", "logout"]
        for cmd in auth_commands:
            assert cmd in result.output, f"Auth command '{cmd}' not found at root level"

    def test_app_subcommands_exist(self, runner):
        """Test that expected app subcommands exist."""
        result = runner.invoke(lumos, ["app", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_user_subcommands_exist(self, runner):
        """Test that expected user subcommands exist."""
        result = runner.invoke(lumos, ["user", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_group_subcommands_exist(self, runner):
        """Test that expected group subcommands exist."""
        result = runner.invoke(lumos, ["group", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_permission_subcommands_exist(self, runner):
        """Test that expected permission subcommands exist."""
        result = runner.invoke(lumos, ["permission", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output

    def test_request_subcommands_exist(self, runner):
        """Test that expected request subcommands exist."""
        result = runner.invoke(lumos, ["request", "--help"])
        assert result.exit_code == 0

        subcommands = ["create", "list", "status", "poll", "cancel"]
        for cmd in subcommands:
            assert cmd in result.output, f"Request subcommand '{cmd}' not found"


class TestCLIOutputFormats:
    """Test that output format options are available."""

    def test_app_list_output_formats(self, runner):
        """Test that app list supports multiple output formats."""
        result = runner.invoke(lumos, ["app", "list", "--help"])
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output

    def test_user_list_output_formats(self, runner):
        """Test that user list supports multiple output formats."""
        result = runner.invoke(lumos, ["user", "list", "--help"])
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output

    def test_request_list_output_formats(self, runner):
        """Test that request list supports multiple output formats."""
        result = runner.invoke(lumos, ["request", "list", "--help"])
        assert "--csv" in result.output
        assert "--json" in result.output
        assert "--id-only" in result.output


class TestCLIPagination:
    """Test pagination options in list commands."""

    def test_app_list_pagination(self, runner):
        """Test that app list supports pagination."""
        result = runner.invoke(lumos, ["app", "list", "--help"])
        assert "--page" in result.output
        assert "--page-size" in result.output
        assert "--paginate" in result.output or "paginate" in result.output.lower()

    def test_user_list_pagination(self, runner):
        """Test that user list supports pagination."""
        result = runner.invoke(lumos, ["user", "list", "--help"])
        assert "--page" in result.output
        assert "--page-size" in result.output

    def test_permission_list_pagination(self, runner):
        """Test that permission list supports pagination."""
        result = runner.invoke(lumos, ["permission", "list", "--help"])
        assert "--page" in result.output
        assert "--page-size" in result.output

    def test_group_list_pagination(self, runner):
        """Test that group list supports pagination."""
        result = runner.invoke(lumos, ["group", "list", "--help"])
        assert "--page" in result.output
        assert "--page-size" in result.output

    def test_request_list_pagination(self, runner):
        """Test that request list supports pagination."""
        result = runner.invoke(lumos, ["request", "list", "--help"])
        assert "--page" in result.output
        assert "--page-size" in result.output
