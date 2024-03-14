import time
from typing import Annotated, List, Optional, Tuple
import typer
from uuid import UUID
from pick import pick
from tabulate import tabulate
import pytz
from functools import reduce
import re

from client import Client
from models import AccessRequest, App, Permission, SupportRequestStatus, User

app = typer.Typer()

client = Client()

@app.callback(invoke_without_command=True)
def request(
    ctx: typer.Context,
    app: Annotated[
        Optional[UUID],
        typer.Option(help="App UUID. Takes precedence over --app-like"),
    ] = None,
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
    permission:Annotated[
        Optional[list[UUID]],
        typer.Option(help="List of permission UUIDs. Takes precedence over --app-like"),
    ] = None,
    length: Annotated[
        Optional[int],
        typer.Option(help="Length of access request in seconds. Don't populate unless you know your app permission's specific settings")
    ] = None,
    app_like: Annotated[
        Optional[str],
        typer.Option(help="App name like--filters apps shown as options when selecting")
    ] = None,
    permission_like: Annotated[
        Optional[str],
        typer.Option(help="Permission name like--filters permissions shown as options when selecting")
    ] = None,
    user_like: Annotated[
        Optional[str],
        typer.Option(help="User name/email like--filters users shown as options when selecting, if the request is not for the current user")
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
        selected_app = get_valid_app(app, app_like)
        typer.echo(f"Selected app {selected_app.user_friendly_label} [{selected_app.id}]\n")
        
        selected_permissions = select_permissions(selected_app.id, permission, permission_like)
        if selected_permissions:
            permissible_durations_set = set(selected_permissions[0].duration_options)
            for permission in selected_permissions[1:]:
                permissible_durations_set = permissible_durations_set.intersection(permission.duration_options)
            if not length:
                length, duration = select_duration(permissible_durations_set)

        if not reason:
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

        if (for_user):
            typer.echo(f"\nTARGET USER")
            typer.echo(f"   {for_user}")
        
        permission_flags = ''
        if selected_permissions:
            permission_flags = ' '.join([f"--permission {permission.id}" for permission in selected_permissions])
        for_user_flag = '--for-me'
        if for_user:
            for_user_flag = '--for-user USER_ID'
        command = f"lumos request --app {selected_app.id} {permission_flags}{(f' --length {length}' if length else '')} --reason \"{reason}\" {for_user_flag}"
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
            wait_max = 10
            while ((status := client.get_request_status(request_id).status) in SupportRequestStatus.PENDING_STATUSES):
                if (wait_max == 0):
                    break
                else:
                    wait_max -= 1
                for num_decimals in range(5):
                    time.sleep(1)
                    print(" ⏰ Waiting for request to complete" + ("." * num_decimals))
            
            if (status == SupportRequestStatus.COMPLETED):
                typer.echo("\n  ✅ Request completed!")
                return
            typer.echo(f"\n  ⏰ Request status: {status}")
            typer.echo(f"Use `lumos request status --request-id {request_id}` to check the status later.")
            

@app.command("status")     
def status(
    request_id: Annotated[
        Optional[str],
        typer.Option(
            help="Request ID",
        ),
    ] = None,
    last: bool = False
) -> None:
    if last:
        current_user_uuid = UUID(client.get_current_user_id())
        access_requests, count, _, _, pages = client.get_access_requests(target_user_id=current_user_uuid)
        if count == 0:
            typer.echo("No pending requests found")
            return
        if (pages > 1):
            access_requests, count, total = client.get_access_requests(
                target_user_id=current_user_uuid,
                page = pages
            )
        print(tabulate([access_requests[0].tabulate()], headers=AccessRequest.headers()), "\n")
        return
    if not request_id:
        request_id = typer.prompt("Please provide a request ID")
    request = client.get_request_status(request_id)
    print(tabulate([request.tabulate()], headers=AccessRequest.headers()), "\n")

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
        typer.echo("\n⏳ Loading your apps ...\n")
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
        app_id = app.id
    return app

def select_permissions(
    app_id: UUID,
    permission_ids: list[UUID] | None, 
    permission_like: str | None = None
) -> List[Permission] | None:
    valid_permissions = get_valid_permissions(app_id, permission_ids)
    if len(valid_permissions) > 0:
        return valid_permissions
    
    typer.echo("\n⏳ Loading permissions for app ...\n")
    done_selecting = False
    valid_permissions_dict: dict[str, Permission] = {}
    while not done_selecting:
        permissions: List[Permission] = []
        while True:
            permissions, count, total = client.get_app_requestable_permissions(app_id=app_id, search_term=permission_like)
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
            description = f"Select at least one permissions{f'(already selected: {already_selected})' if already_selected else ''}\nUse SPACE or right arrow to select, ENTER to confirm"
            selected = pick(permissions, description, multiselect=True, min_selection_count=1)
            for option, _ in selected:
                valid_permissions_dict[option.id] = option
        elif count == 1:
            valid_permissions_dict[permissions[0].id] = permissions[0]
        if not permission_like:
            break
        if typer.confirm("Done selecting permissions?", abort=False, default=True):
            done_selecting = True
        else:
            permission_like = typer.prompt("Give me something to search on")
    return list(valid_permissions_dict.values())
            

def get_valid_permissions(app_id: UUID, permission_ids: list[UUID] | None) -> list[Permission]:
    valid_permissions: list[Permission] = []
    if not permission_ids:
        return []
    for permission_id in permission_ids:
        if not (permission := client.get_app_requestable_permission(permission_id)):
            return []
        if not permission.app_id.__eq__(app_id):
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
    typer.echo(f"Selected duration: {duration}{f' ({time_in_seconds} seconds)' if time_in_seconds else ''}")
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
    
    typer.echo("\nREQUEST DETAILS")
    typer.echo(tabulate([response.tabulate()], headers=AccessRequest.headers()))

    typer.echo("\nYour request is in progress! 🏃🌴")

    return response.id

if __name__ == "__main__":
    app()