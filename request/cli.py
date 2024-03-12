from typing import List, Optional, Tuple
import typer
from uuid import UUID
from pick import pick
from tabulate import tabulate
import pytz
from functools import reduce
import re

from client import Client
from models import AccessRequest, App, Permission

app = typer.Typer()

client = Client()

@app.callback(invoke_without_command=True)
def request(
    ctx: typer.Context,
    app: Optional[UUID] = None,
    app_like: Optional[str] = None,
    reason: Optional[str] = None,
    for_user: Optional[UUID] = None,
    permission: Optional[list[UUID]] = None,
    permission_like: Optional[str] = None,
    user_like: Optional[str] = None,
    length: Optional[int] = None,
) -> None:
    if ctx.invoked_subcommand is None:
        if not typer.confirm("This request is for you?", abort=False, default=True):
            users, count = client.get_users(like=user_like)
            description = "Select a user"
            if (len(users) < count):
                description += "\nThere are {count - len(users)} more users that match your search. Use --user_like to search.\n"
            for_user, _ = pick(users, description)
            typer.echo(f"Selected user {for_user.email}\n")
            for_user = for_user.id
        
        # Validate parameters or interactively input them
        selected_app = get_valid_app(app, app_like)
        typer.echo(f"Selected app {selected_app.user_friendly_label} [{selected_app.id}]\n")
        
        selected_permissions = select_permissions(selected_app.id, permission, permission_like)
        if not selected_permissions:
            return
        
        permissible_durations_set = set(selected_permissions[0].duration_options)
        
        for permission in selected_permissions[1:]:
            permissible_durations_set = permissible_durations_set.intersection(permission.duration_options)

        if not length:
            length, duration = select_duration(permissible_durations_set)

        if not reason:
            reason = typer.prompt("Enter your business justification for the request")

        typer.echo("\nAPP")
        typer.echo(f"   {selected_app.user_friendly_label} [{selected_app.id}]")
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
        
        create_access_request(
            app_id=selected_app.id, 
            requestable_permission_ids=[p.id for p in selected_permissions],
            note=reason,
            expiration=length,
            target_user_id=for_user)
        
        typer.echo("If you need to make this same request in the future, use:")
        permission_flags = ""
        for permission in selected_permissions:
            permission_flags += f" --permission {permission.id}"
        typer.echo(f"\n   `lumos request --app {selected_app.id}{permission_flags}{(f' --length {length}' if length else '')} --reason \"{reason}\"{' --for-user USER_ID]' if for_user else ''}`\n")

def get_valid_app(app_id: Optional[UUID] = None, app_like: Optional[str] = None) -> App:
    app = None
    while not app_id or not (app := client.get_appstore_app(app_id)):
        typer.echo("\n⏳ Loading your apps ...\n")
        apps, count = client.get_appstore_apps(name_search=app_like)
        description = f"Select an app"
        if (len(apps) < count):
            description += f"\n\n({count - len(apps)} not shown--use `lumos list apps` to search all apps)"
        app, _ = pick(apps, description)
        app_id = app.id
    return app

def select_permissions(app_id: UUID, permission_ids: list[UUID] | None, permission_like: str | None = None) -> List[Permission]:
    valid_permissions = get_valid_permissions(app_id, permission_ids)
    if len(valid_permissions) > 0:
        return valid_permissions
    
    typer.echo("\n⏳ Loading permissions for app ...\n")
    permissions, count = client.get_app_requestable_permissions(app_id=app_id, search_term=permission_like)
    description = f"Select at least one permission"
    if (len(permissions) < count):
        description += f"\n\n({count - len(permissions)} not shown--use `lumos list permissions --app {app_id}` to search all permissions)"
    if len(permissions) > 1:
        selected = pick(permissions, description, multiselect=True, min_selection_count=1)
        return [option for option, _ in selected]
    elif len(permissions) == 1:
        return [permissions[0]]
    else:
        typer.echo("No permissions found for this app")
        return []
    

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
        duration, _ = pick(list(durations), "Select duration", multiselect=False, min_selection_count=1)
    
    time_in_seconds = None
    if match := re.match(r"(\d+) ", duration):
        time_in_seconds = int(match.group(1)) * 60 * 60
        if (re.match(r".*days", duration)):
            time_in_seconds = 24 * time_in_seconds
    typer.echo(f"Selected duration: {duration}{f' ({time_in_seconds} seconds)'}")
    return time_in_seconds, duration
        

def create_access_request(
    app_id: UUID,
    requestable_permission_ids: List[UUID],
    note: str,
    expiration: Optional[int] = None,
    target_user_id: Optional[UUID] = None
) -> None:
    request = client.create_access_request(
        app_id=app_id,
        permission_ids=requestable_permission_ids,
        note=note,
        expiration_in_seconds=expiration,
        target_user_id=target_user_id
    )
    if request:
        print("\nREQUEST DETAILS")
        print(tabulate([request.tabulate()], headers=AccessRequest.headers()), "\n")

    print("\nYour request is in progress! 🏃🌴")

if __name__ == "__main__":
    app()