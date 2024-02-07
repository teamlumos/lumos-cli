from typing import List, Optional
import typer

from request.client import Client, App, Permission

app = typer.Typer()

client = Client()

@app.callback(invoke_without_command=True)
def request(
    ctx: typer.Context,
    app: Optional[int] = None,
    user: Optional[int] = None,
    permission: Optional[int] = None,
    length: Optional[int] = None,
) -> None:
    if ctx.invoked_subcommand is None:
        # Validate parameters or interactively input them
        if not app:
            app = typer.prompt("Enter the domain app id")
        if not user:
            user = typer.prompt("Enter the user id")
        if not permission:
            permission = typer.prompt("Enter the permission id")
        if not length:
            length = typer.prompt("Enter the access length")
        print(f"Requesting app {app} for {user} to access permission {permission} for {length} seconds")
        

@app.command()
def list_permissions(
    app_id: str
) -> None:
    print(app_id)
    permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app_id)
    for permission in permissions:
        print(permission)

@app.command()
def list_apps(
) -> None:
    apps: List[App] = client.get_appstore_apps()
    for app in apps:
        print(app)

@app.command()
def create_access_request(
    app_id: str,
    requestable_permission_id: str,
    target_user_id: str,
    note: str,
    expiration_in_seconds: Optional[int] = None
) -> List[App]:
    resp = client.create_access_request(
        app_id=app_id,
        permission_id=requestable_permission_id,
        target_user_id=target_user_id,
        note=note,
       # expiration_in_seconds=expiration_in_seconds,
    )
    print("started request")
    return

@app.command()
def list_access_lengths(
    app: int,
    permission: int
) -> None:
    print(f"Listing access lengths for app {app} and permission {permission}")
    return

if __name__ == "__main__":
    app()