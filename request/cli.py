import time
from typing import Annotated, List, Optional, Tuple
import typer
from uuid import UUID
from pick import pick
from tabulate import tabulate
import re

from common.client import ApiClient
from common.models import AccessRequest, App, Permission, SupportRequestStatus, User

app = typer.Typer()
POLLING_INTERVAL = 6
client = ApiClient()

@app.callback(invoke_without_command=True)
def request(
    ctx: typer.Context,
    reason: Annotated[
        Optional[str],
        typer.Option(help="Business justification for request")
    ] = None,
    for_user: Annotated[
        Optional[UUID],
        typer.Option(help="UUID of user for whom to request access. Takes precedence over --user-like"),
    ] = None,
    for_me: Annotated[
        Optional[bool],
        typer.Option(help="Makes the request for the current user.")
    ] = None,
    app: Annotated[
        Optional[UUID],
        typer.Option(help="App UUID. Takes precedence over --app-like"),
    ] = None,
    permission:Annotated[
        Optional[list[UUID]],
        typer.Option(help="List of permission UUIDs. Takes precedence over --permission-like"),
    ] = None,
    length: Annotated[
        Optional[int],
        typer.Option(help="Length of access request in seconds. Don't populate unless you know your app permission's specific settings")
    ] = None,
    user_like: Annotated[
        Optional[str],
        typer.Option(help="User name/email like--filters users shown as options when selecting, if the request is not for the current user")
    ] = None,
    app_like: Annotated[
        Optional[str],
        typer.Option(help="App name like--filters apps shown as options when selecting")
    ] = None,
    permission_like: Annotated[
        Optional[str],
        typer.Option(help="Permission name like--filters permissions shown as options when selecting")
    ] = None,
    wait: Annotated[
        Optional[bool],
        typer.Option(help="Wait for the request to complete")
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(help="Print the request command without actually making the request")
    ] = False
) -> None:
    if ctx.invoked_subcommand is None:
        if for_me is not True and not typer.confirm("This request is for you?", abort=False, default=True):
            for_user = select_user(user_like)
        
        # Validate parameters or interactively input them
        selected_app: App = get_valid_app(app, app_like)
        typer.echo(f"APP: {selected_app.user_friendly_label} [{selected_app.id}]\n")
        
        selected_permissions = select_permissions(selected_app, permission, permission_like)
        if selected_permissions:
            permissible_durations_set = set(selected_permissions[0].duration_options)
            for permission in selected_permissions[1:]:
                permissible_durations_set = permissible_durations_set.intersection(permission.duration_options)
            if not length:
                length, duration = select_duration(permissible_durations_set)

        while not reason or len(reason) < 1:
            reason = typer.prompt("\nEnter your business justification for the request")

        typer.echo("\nAPP")
        typer.echo(f"   {selected_app.user_friendly_label} [{selected_app.id}]")
        if selected_permissions:
            typer.echo("\nPERMISSIONS")
            for permission in selected_permissions:
                typer.echo(f"   {permission.label} [{permission.id}]")
        typer.echo("\nDURATION")
        typer.echo(f"   {(length/(60*60) if length else 'Unlimited')} hours")
        typer.echo("\nREASON")
        typer.echo(f"   {reason}")

        if for_user:
            typer.echo(f"\nTARGET USER")
            typer.echo(f"   {for_user}")

        permission_flags = ''
        if selected_permissions:
            permission_flags = ' '.join([f"--permission {permission.id}" for permission in selected_permissions])

        command = f"lumos request --app {selected_app.id} {permission_flags} --reason \"{reason}\""
        if length:
            command += f" --length {length}"
        for_user_flag = '--for-me'
        if for_user:
            for_user_flag = '--for-user USER_ID'
        command += f" {for_user_flag}"
        if wait:
            command += " --wait"
        if dry_run:
            typer.echo(f"\nCOMMAND")
            typer.echo(f"   {command}")
            return
        
        typer.echo("\nIf you need to make this same request in the future, use:")
        typer.echo(f"\n   `{command}`\n")
        
        request_id = create_access_request(
            app_id=selected_app.id, 
            requestable_permission_ids=[p.id for p in selected_permissions] if selected_permissions else None,
            note=reason,
            expiration=length,
            target_user_id=for_user)
        
        if wait and request_id:
            _poll(request_id)

@app.command("status")     
def status(
    request_id: Annotated[
        Optional[str],
        typer.Option(
            help="Request ID",
        ),
    ] = None,
    last: bool = False,
    status_only: Annotated[
        Optional[bool],
        typer.Option(
            help="Output status only",
        ),
    ] = None,
    permission_only: Annotated[
        Optional[bool],
        typer.Option(
            help="Output permission only",
        ),
    ] = None,
    id_only: Annotated[
        Optional[bool],
        typer.Option(
            help="Output request ID only",
        ),
    ] = None,
) -> None:
    request: AccessRequest | None
    if last:
        current_user_uuid = client.get_current_user_id()
        access_requests, count, _, _, pages = client.get_access_requests(target_user_id=current_user_uuid)
        if count == 0:
            typer.echo("No pending requests found")
            return
        if (pages > 1):
            access_requests, count, total, _, _ = client.get_access_requests(
                target_user_id=current_user_uuid,
                page = pages
            )
        request = access_requests[0]
    else:
        request_uuid: UUID | None = None
        while not request_uuid:
            try:
                request_uuid = UUID(request_id)
                break
            except:
                if request_id:
                    typer.echo("Invalid request ID")
                request_id = None
            request_id = typer.prompt("Please provide a request ID")
            
        request = client.get_request_status(request_uuid)
    if not request:
        typer.echo("Request not found")
        return
    if status_only:
        typer.echo(request.status)
        return
    if permission_only:
        if request.requestable_permissions:
            for permission in request.requestable_permissions:
                typer.echo(permission.label)
        return
    if last and id_only:
        typer.echo(request.status)
        return
    print(tabulate([request.tabulate()], headers=AccessRequest.headers()), "\n")

@app.command("poll", help="Poll a request by ID for up to 5 minutes")
def poll(
    request_id: UUID,
    wait: Annotated[
        Optional[int],
        typer.Option(help="How many minutes to wait. Max 5.")
    ] = 2
) -> None:
    _poll(request_id, (wait or 2) * 60)

def _poll(request_id: UUID, wait_seconds: int = 120):
    if wait_seconds == 0 or wait_seconds > 300:
        wait_max = 120
    while ((request := client.get_request_status(request_id)) is not None):
        if request.status not in SupportRequestStatus.PENDING_STATUSES or wait_max <= 0:
            break
        wait_max -= POLLING_INTERVAL
        for num_decimals in range(POLLING_INTERVAL):
            time.sleep(1)
            print(" ⏰ Waiting for request to complete" + ("." * num_decimals) + (' ' * (POLLING_INTERVAL-num_decimals)), end='\r')

    if not request:
        typer.echo("Request not found")
        raise typer.Exit(1)

    if (request.status == SupportRequestStatus.COMPLETED):
        typer.echo(" ✅ Request completed!")
        return
    typer.echo(f" ⏰ Request status: {request.status}" + (' ' * 20) + "\n")
    typer.echo(f"Use `lumos request status --request-id {request_id}` to check the status later.")


def select_user(user_like: Optional[str] = None) -> UUID:
    users: List[User] = []
    for_user: User | None = None
    while for_user is None:
        while True:
            users, count, total = client.get_users(like=user_like)
            if (total == 0):
                if user_like:
                    typer.echo(f"No users found for '{user_like}'")
                    user_like = typer.prompt("Give me something to search on")
                else:
                    typer.echo("No users found")
                    raise typer.Exit(1)
            elif count == 1:
                for_user = users[0]
                break
            elif (count < total):
                user_like = typer.prompt(f"Too many users to show. Give me something to search on")
            else:
                break
        if not for_user:
            description = "Select user (use ENTER to confirm)"
            for_user, _ = pick(users, description)
    typer.echo(f"Selected user {for_user.email} [{for_user.id}]\n")
    return for_user.id


def get_valid_app(app_id: Optional[UUID] = None, app_like: Optional[str] = None) -> App:
    app = None
    while not app_id or not (app := client.get_appstore_app(app_id)):
        print("\n⏳ Loading your apps ...", end='\r')
        apps: list[App] = []
        while True:
            apps, count, total = client.get_appstore_apps(name_search=app_like)
            if (total == 0):
                if app_like:
                    typer.echo(f"No apps found for '{app_like}'")
                    app_like = typer.prompt("Give me something to search on")
                else:
                    typer.echo("No apps found")
                    raise typer.Exit(1)
            elif (count < total):
                app_like = typer.prompt(f"Too many apps to show. Give me something to search on")
            else:
                break
        if count == 1:
            app = apps[0]
        else:
            app, _ = pick(apps, f"Select an app (press ENTER to confirm)")
        if app:
            app_id = app.id
    return app

def select_permissions(
    app: App,
    permission_ids: list[UUID] | None, 
    permission_like: str | None = None
) -> List[Permission] | None:
    valid_permissions = get_valid_permissions(app, permission_ids)
    if len(valid_permissions) > 0:
        return valid_permissions
    print("\n⏳ Loading permissions for app ...", end='\r')
    done_selecting = False
    valid_permissions_dict: dict[str, Permission] = {}
    while not done_selecting:
        permissions: List[Permission] = []
        while True:
            permissions, count, total = client.get_app_requestable_permissions(app_id=app.id, search_term=permission_like)
            if (total == 0):
                if permission_like:
                    permission_like = typer.prompt(f"No permissions found for '{permission_like}'. Give me something to search on")
                else:
                    typer.echo("No permissions found (you're just requesting the app)")
                    return None
            elif (count < total):
                permission_like = typer.prompt("Too many permissions to show. Give me something to search on")
            else:
                break
        if count > 1:
            already_selected = ', '.join([p.label for p in valid_permissions_dict.values()])
            if app.allow_multiple_permission_selection:
                description = f"Select at least one permissions{f'(already selected: {already_selected})' if already_selected else ''}\nUse SPACE or right arrow to select, ENTER to confirm"
                selected = pick(permissions, description, multiselect=True, min_selection_count=1)
                for option, _ in selected:
                    valid_permissions_dict[str(option.id)] = option
            else:
                option, _ = pick(permissions, "Select permission (use ENTER to confirm)")
                valid_permissions_dict[str(option.id)] = option
        elif count == 1:
            permission = permissions[0]
            valid_permissions_dict[str(permission.id)] = permission
            permission_like = None
        typer.echo("PERMISSIONS:                          ")
        for permission in valid_permissions_dict.values():
            typer.echo(f"   {permission.label} [{permission.id}]")
        if not permission_like or not app.allow_multiple_permission_selection:
            break
        if typer.confirm("Done selecting permissions?", abort=False, default=True):
            done_selecting = True
        else:
            permission_like = typer.prompt("Give me something to search on")
    return list(valid_permissions_dict.values())
            

def get_valid_permissions(app: App, permission_ids: list[UUID] | None) -> list[Permission]:
    valid_permissions: list[Permission] = []
    if not permission_ids:
        return []
    if len(permission_ids) > 1 and not app.allow_multiple_permission_selection:
        return []
    for permission_id in permission_ids:
        if not (permission := client.get_app_requestable_permission(permission_id)):
            return []
        if not permission.app_id.__eq__(app.id):
            return []
        valid_permissions.append(permission)
    return valid_permissions

def select_duration(durations: set[str]) -> Tuple[int | None, str]:
    duration: str = ""
    if (len(durations) == 1):
        duration = list(durations)[0]
    elif (len(durations) > 1):
        duration, _ = pick(list(durations), "Select duration (use ENTER to confirm)", multiselect=False, min_selection_count=1)
    
    time_in_seconds = None
    if match := re.match(r"(\d+) ", duration):
        time_in_seconds = int(match.group(1)) * 60 * 60
        if (re.match(r".*days", duration)):
            time_in_seconds = 24 * time_in_seconds
    typer.echo(f"DURATION: {duration}{f' ({time_in_seconds} seconds)' if time_in_seconds else ''}")
    return time_in_seconds, duration
        

def create_access_request(
    app_id: UUID,
    requestable_permission_ids: List[UUID] | None,
    note: str,
    expiration: Optional[int] = None,
    target_user_id: Optional[UUID] = None
) -> UUID | None:
    response = client.create_access_request(
        app_id=app_id,
        permission_ids=requestable_permission_ids,
        note=note,
        expiration_in_seconds=expiration,
        target_user_id=target_user_id
    )
    if not response:
        return None
    
    typer.echo(f"\nYour request (ID {response.id}) is in progress! 🏃🌴\n")

    return response.id

if __name__ == "__main__":
    app()
