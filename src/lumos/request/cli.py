import re
import time
from uuid import UUID

from click_extra import Context, confirm, echo, group, option, pass_context, prompt
from pick import pick
from tabulate import tabulate

from lumos.common.client import ApiClient
from lumos.common.helpers import authenticate
from lumos.common.models import (
    AccessRequest,
    App,
    Permission,
    ProvisioningMethodOption,
    SupportRequestStatus,
    User,
)

POLLING_INTERVAL = 6
client = ApiClient()


@group(name="request", invoke_without_command=True)
@pass_context
@option("--reason", default=None, help="Business justification for request")
@option(
    "--for-user",
    default=None,
    type=str,
    help="UUID of user for whom to request access. Takes precedence over --user-like",
)
@option("--for-me", is_flag=True, help="Makes the request for the current user.")
@option(
    "--mine",
    is_flag=True,
    help="Makes the request for the current user. Duplicate of --for-me for convenience.",
)
@option("--app", default=None, type=str, help="App UUID. Takes precedence over --app-like")
@option(
    "--permission",
    multiple=True,
    type=str,
    help="List of permission UUIDs. Takes precedence over --permission-like",
)
@option(
    "--length",
    default=None,
    help="Length of access request in seconds, or a string like '12 hours', '2d', 'unlimited', etc. Every app/permission has different configurations.",
)
@option(
    "--user-like",
    default=None,
    help="User name/email like--filters users shown as options when selecting, if the request is not for the current user",
)
@option(
    "--app-like",
    default=None,
    help="App name like--filters apps shown as options when selecting",
)
@option(
    "--permission-like",
    default=None,
    help="Permission name like--filters permissions shown as options when selecting",
)
@option("--wait/--no-wait", default=None, help="Wait for the request to complete")
@option(
    "--dry-run",
    is_flag=True,
    help="Print the request command without actually making the request",
)
@authenticate
def request(
    ctx: Context,
    reason: str | None,
    for_user: str | None,
    for_me: bool,
    mine: bool,
    app: str | None,
    permission: tuple,
    length: str | None,
    user_like: str | None,
    app_like: str | None,
    permission_like: str | None,
    wait: bool | None,
    dry_run: bool,
) -> None:
    """Request access to an app."""
    if ctx.invoked_subcommand is None:
        for_user_uuid = None
        if for_me is not True and mine is not True:
            if user_like is not None or not confirm("This request is for you?", default=True):
                for_user_uuid = select_user(user_like)
        elif for_user:
            for_user_uuid = UUID(for_user)

        # Validate parameters or interactively input them
        app_uuid = UUID(app) if app else None
        selected_app: App = get_valid_app(app_uuid, app_like)
        app_settings = client.get_appstore_app_setting(selected_app.id)
        duration_options = set(app_settings.provisioning.time_based_access)
        selected_permissions = None

        permission_uuids = [UUID(p) for p in permission] if permission else None

        if app_settings.provisioning.groups_provisioning == ProvisioningMethodOption.GROUPS_AND_VISIBLE:
            selected_permissions = select_permissions(
                selected_app,
                app_settings.provisioning.allow_multiple_permission_selection,
                permission_uuids,
                permission_like,
            )
            if selected_permissions:
                duration_options = set(selected_permissions[0].duration_options)
                for perm in selected_permissions[1:]:
                    duration_options = duration_options.intersection(perm.duration_options)

        duration, duration_friendly = get_duration(duration_options, length)

        while not reason or len(reason) < 1:
            reason = prompt("\nEnter your business justification for the request")

        if wait is None:
            wait = confirm("Do you want to wait for the request to complete?", default=True)

        echo("\nAPP")
        echo(f"   {selected_app.user_friendly_label} [{selected_app.id}]")
        if selected_permissions:
            echo("\nPERMISSIONS")
            for perm in selected_permissions:
                echo(f"   {perm.label} [{perm.id}]")
        echo("\nDURATION")
        echo(f"   {duration_friendly or 'Unlimited'} {f'({duration} seconds)' if duration else ''}")
        echo("\nREASON")
        echo(f"   {reason}")

        if for_user_uuid:
            echo("\nTARGET USER")
            echo(f"   {for_user_uuid}")

        permission_flags = ""
        if selected_permissions:
            permission_flags = " ".join([f"--permission {perm.id}" for perm in selected_permissions])

        command_str = f'lumos request --app {selected_app.id} {permission_flags} --reason "{reason}"'
        if duration:
            command_str += f" --length {duration}"
        for_user_flag = "--for-me"
        if for_user_uuid:
            for_user_flag = "--for-user USER_ID"
        command_str += f" {for_user_flag}"
        if wait:
            command_str += " --wait"
        else:
            command_str += " --no-wait"
        if dry_run:
            echo("\nCOMMAND")
            echo(f"   {command_str}")
            return

        echo("\nIf you need to make this same request in the future, use:")
        echo(f"\n   `{command_str}`\n")

        request_id = create_access_request(
            app_id=selected_app.id,
            requestable_permission_ids=([p.id for p in selected_permissions] if selected_permissions else None),
            note=reason,
            expiration=duration,
            target_user_id=for_user_uuid,
        )

        if wait and request_id:
            _poll(request_id)


@request.command(
    "status",
    help="Check the status of a request by ID or `--last` for the most recent request",
)
@option("--request-id", default=None, help="Request ID")
@option("--last", is_flag=True, help="Get the last request")
@option("--status-only", is_flag=True, help="Output status only")
@option("--permission-only", is_flag=True, help="Output permission only")
@option("--id-only", is_flag=True, help="Output request ID only")
@authenticate
def status(
    request_id: str | None,
    last: bool,
    status_only: bool,
    permission_only: bool,
    id_only: bool,
) -> None:
    access_request: AccessRequest | None
    if last:
        access_requests, count, _, _, _ = client.get_access_requests(target_user_id=client.get_current_user_id())
        if count == 0:
            echo("No pending requests found")
            return
        access_request = access_requests[0]
    else:
        request_uuid: UUID | None = None
        while not request_uuid:
            try:
                request_uuid = UUID(request_id)
                break
            except ValueError:
                if request_id:
                    echo("Invalid request ID")
                request_id = None
            request_id = prompt("Please provide a request ID")

        access_request = client.get_request_status(request_uuid)
    if not access_request:
        echo("Request not found")
        return
    if status_only:
        echo(access_request.status)
        return
    if permission_only:
        if access_request.requestable_permissions:
            for perm in access_request.requestable_permissions:
                echo(perm.label)
        return
    if last and id_only:
        echo(access_request.status)
        return
    print(tabulate([access_request.tabulate()], headers=AccessRequest.headers()), "\n")


@request.command("poll", help="Poll a request by ID for up to 5 minutes")
@option("--request-id", default=None, type=str, help="Request ID")
@option("--wait", default=2, help="How many minutes to wait. Max 5.")
@authenticate
def poll(request_id: str | None, wait: int) -> None:
    request_uuid = UUID(request_id) if request_id else None
    while not request_uuid:
        request_id_str = prompt("Please provide a request ID")
        request_uuid = UUID(request_id_str)

    _poll(request_uuid, (wait or 2) * 60)


def _poll(request_id: UUID, wait_max: int = 120):
    if wait_max < 10 or wait_max > 300:
        wait_max = 120
    while (access_request := client.get_request_status(request_id)) is not None:
        if access_request.status not in SupportRequestStatus.PENDING_STATUSES or wait_max <= 0:
            break
        wait_max -= POLLING_INTERVAL
        for num_decimals in range(POLLING_INTERVAL):
            time.sleep(1)
            print(
                " ⏰ Waiting for request to complete"
                + ("." * num_decimals)
                + (" " * (POLLING_INTERVAL - num_decimals)),
                end="\r",
            )

    if not access_request:
        echo("Request not found")
        raise SystemExit(1)

    if access_request.status == SupportRequestStatus.COMPLETED:
        echo(" ✅ Request completed!")
        return
    echo(f" ⏰ Request status: {access_request.status}" + (" " * 20) + "\n")
    echo(f"Use `lumos request status --request-id {request_id}` to check the status later.")


@request.command("cancel", help="Cancel a request by ID")
@option("--request-id", default=None, type=str, help="Request ID")
@option("--reason", default=None, help="Reason for cancellation")
@authenticate
def cancel(request_id: str | None, reason: str | None) -> None:
    request_uuid = None
    while not request_uuid:
        if not request_id:
            request_id = prompt(
                "Please provide a request ID or press enter to look up a request",
                default="",
                show_default=False,
            )
        if not request_id:
            pending_requests, _, _, _, _ = client.get_access_requests(
                client.get_current_user_id(),
                SupportRequestStatus.PENDING_STATUSES,
                all=True,
            )
            if len(pending_requests) == 0:
                echo("No pending requests found")
                raise SystemExit(1)
            access_request, _ = pick(pending_requests, "Select a request to cancel")
            request_uuid = access_request.id
        else:
            request_uuid = UUID(request_id)

    if (
        access_request := client.get_request_status(request_uuid)
    ) is not None and access_request.status not in SupportRequestStatus.PENDING_STATUSES:
        echo(f"Request is not pending, cannot cancel. Status is {access_request.status}.")
        raise SystemExit(1)

    client.cancel_access_request(request_uuid, reason)
    echo("Request cancelled! 🚫")


def select_user(user_like: str | None = None) -> UUID:
    users: list[User] = []
    for_user: User | None = None
    while for_user is None:
        while True:
            users, count, total = client.get_users(like=user_like)
            if total == 0:
                if user_like:
                    echo(f"No users found for '{user_like}'")
                    user_like = prompt("🔍 Give me something to search on")
                else:
                    echo("No users found")
                    raise SystemExit(1)
            elif count == 1:
                for_user = users[0]
                break
            elif count < total:
                echo("Too many users to show.")
                user_like = prompt("🔍 Give me something to search on")
            else:
                break
        if not for_user:
            description = "Select user (use ENTER to confirm)"
            for_user, _ = pick(users, description)
    echo(f"USER: {for_user.email} [{for_user.id}]\n")
    return for_user.id


def get_valid_app(app_id: UUID | None = None, app_like: str | None = None) -> App:
    app = None
    while not app_id or not (app := client.get_appstore_app(app_id)):
        apps: list[App] = []
        while True:
            print("\n⏳ Loading your apps ...", end="\r")
            apps, count, total = client.get_appstore_apps(name_search=app_like, page_size=25)
            print("                          ", end="\r")
            if total == 0:
                if app_like:
                    app_like = prompt(f"No apps found for '{app_like}'\n🔍 Give me something to search on")
                else:
                    echo("No apps found")
                    raise SystemExit(1)
            elif count < total:
                echo("")
                app_like = prompt("Too many apps to show.\n🔍 Give me something to search on")
            else:
                break
        if count == 1:
            app = apps[0]
        else:
            app, _ = pick(apps, "Select an app (press ENTER to confirm)")
        if app:
            app_id = app.id
    echo(f"APP: {app.user_friendly_label} [{app.id}]\n")
    return app


def select_permissions(
    app: App,
    allow_multiple_permission_selection: bool,
    permission_ids: list[UUID] | None,
    permission_like: str | None = None,
) -> list[Permission] | None:
    valid_permissions = get_valid_permissions(app, permission_ids, allow_multiple_permission_selection)
    if len(valid_permissions) > 0:
        return valid_permissions
    done_selecting = False
    valid_permissions_dict: dict[str, Permission] = {}
    while not done_selecting:
        permissions: list[Permission] = []
        while True:
            print("\n⏳ Loading permissions for app ...", end="\r")
            permissions, count, total = client.get_app_requestable_permissions(
                app_id=app.id, search_term=permission_like, page_size=25
            )
            print("                                    ", end="\r")
            if total == 0:
                if permission_like:
                    permission_like = prompt(
                        f"No permissions found for '{permission_like}'\n🔍 Give me something to search on"
                    )
                else:
                    echo("No permissions found (you're just requesting the app)")
                    return None
            elif count < total:
                permission_like = prompt("Too many permissions to show.\n🔍 Give me something to search on")
            else:
                break
        if count > 1:
            already_selected = ", ".join([p.label for p in valid_permissions_dict.values()])
            if allow_multiple_permission_selection:
                description = f"Select at least one permissions\n{f'(already selected: {already_selected})' if already_selected else ''}\nUse SPACE or right arrow to select, ENTER to confirm"
                selected = pick(permissions, description, multiselect=True, min_selection_count=1)  # type: ignore[misc]
                for option, _ in selected:
                    valid_permissions_dict[str(option.id)] = option
            else:
                option, _ = pick(permissions, "Select permission (use ENTER to confirm)")
                valid_permissions_dict[str(option.id)] = option
        elif count == 1:
            permission = permissions[0]
            valid_permissions_dict[str(permission.id)] = permission
            permission_like = None
        echo("PERMISSIONS:                          ")
        for permission in valid_permissions_dict.values():
            echo(f"   {permission.label} [{permission.id}]")
        if not permission_like or not allow_multiple_permission_selection:
            break
        if confirm("Done selecting permissions?", default=True):
            done_selecting = True
        else:
            permission_like = prompt("🔍 Give me something to search on")
    return list(valid_permissions_dict.values())


def get_valid_permissions(
    app: App,
    permission_ids: list[UUID] | None,
    allow_multiple_permission_selection: bool,
) -> list[Permission]:
    valid_permissions: list[Permission] = []
    if not permission_ids:
        return []
    if len(permission_ids) > 1 and not allow_multiple_permission_selection:
        return []
    for permission_id in permission_ids:
        if not (permission := client.get_app_requestable_permission(permission_id)):
            return []
        if not permission.app_id.__eq__(app.id):
            return []
        valid_permissions.append(permission)
    return valid_permissions


def select_duration(durations: set[str], duration_friendly: str | None) -> tuple[int | None, str]:
    selected: str = ""
    if len(durations) == 1:
        selected = next(iter(durations))
    elif duration_friendly in durations:
        selected = duration_friendly
    elif len(durations) > 1:
        selected, _ = pick(
            list(durations),
            "Select duration (use ENTER to confirm)",
            multiselect=False,
            min_selection_count=1,
        )

    time_in_seconds = None
    if match := re.match(r"(\d+) ", selected):
        time_in_seconds = int(match.group(1)) * 60 * 60
        if re.match(r".*days", selected):
            time_in_seconds = 24 * time_in_seconds
    echo(f"DURATION: {selected}{f' ({time_in_seconds} seconds)' if time_in_seconds else ''}")
    return time_in_seconds, selected


def parse_duration(duration: str) -> tuple[int | None, str]:
    time_in_seconds = None
    if match := re.match(r"(\d+) ", duration):
        time_in_seconds = int(match.group(1)) * 60 * 60
        if re.match(r".* d", duration):
            time_in_seconds = 24 * time_in_seconds
    return time_in_seconds, duration.replace(" ", "").lower()


def get_duration(possible_durations: set[str], input_length: str | None) -> tuple[int | None, str]:
    duration_friendly: str | None = None
    durations = {}
    for possible_duration in possible_durations:
        length, key = parse_duration(possible_duration)

        durations[key] = {
            "label": possible_duration,
            "length": length,
        }
    if input_length:
        try:
            duration = int(input_length)
            duration_friendly = None
            for _key, v in durations.items():
                if v["length"] == duration:
                    duration_friendly = v["label"]
                    break
        except ValueError:
            for key, v in durations.items():
                if key.startswith(input_length.replace(" ", "").lower()):
                    duration_friendly = v["label"]
                    break

    duration, duration_friendly = select_duration(possible_durations, duration_friendly)
    return duration, duration_friendly


def create_access_request(
    app_id: UUID,
    requestable_permission_ids: list[UUID] | None,
    note: str,
    expiration: int | None = None,
    target_user_id: UUID | None = None,
) -> UUID | None:
    response = client.create_access_request(
        app_id=app_id,
        permission_ids=requestable_permission_ids,
        note=note,
        expiration_in_seconds=expiration,
        target_user_id=target_user_id,
    )
    if not response:
        return None

    echo(f"\nYour request (ID {response.id}) is in progress! 🏃🌴\n")

    return response.id


if __name__ == "__main__":
    request()
