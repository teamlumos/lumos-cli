from typing import List, Optional
import typer
from uuid import UUID
from tabulate import tabulate
from pick import pick

from request.client import AccessRequest, Client, App, Permission

app = typer.Typer()

client = Client()

@app.callback(invoke_without_command=True)
def request(
    ctx: typer.Context,
    app: Optional[UUID] = None,
    reason: Optional[str] = None,
    user: Optional[UUID] = None,
    permission: Optional[UUID] = None,
    length: Optional[int] = None,
) -> None:
    if ctx.invoked_subcommand is None:
        # Validate parameters or interactively input them
        if not app:
            apps: List[App] = client.get_appstore_apps()
            option, _ = pick(apps, "Select an app")
            app = option.id
            print(f"Selected app {app}")

        if not permission:
            # permission = typer.prompt("Enter the permission id")
            permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app)
            if len(permissions) > 1:
                option, _ = pick(permissions, "Select a permission")
                permission = option.id
            else:
                permission = permissions[0].id
            print(f"Selected permission {permission}\n")
        
        if not reason:
            reason = typer.prompt("Enter your business justification for the request")

        create_access_request(app_id=app, requestable_permission_id=permission, target_user_id=user, note=reason, expiration=length)
        

@app.command()
def list_permissions(
    app_id: str
) -> None:
    permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app_id)
    print(tabulate([[permission.label, permission.id] for permission in permissions], headers=["Permission", "UUID"]), "\n")

@app.command()
def list() -> None:
    access_requests: List[AccessRequest] = client.get_access_requests()
    print(tabulate([[ar.app_name, ar.status, ar.requested_at, ar.supporter_user.email if ar.supporter_user else "Pending"] for ar in access_requests], headers=["App", "Request Status", "Requested At", "Approver Email"]), "\n")

@app.command()
def list_apps(
) -> None:
    apps: List[App] = client.get_appstore_apps()
    print(tabulate([[app.user_friendly_label, app.id] for app in apps], headers=["App", "UUID"]), "\n")

def create_access_request(
    app_id: str,
    requestable_permission_id: str,
    target_user_id: str,
    note: str,
    expiration: Optional[int] = None
) -> List[App]:
    resp = client.create_access_request(
        app_id=app_id,
        permission_id=requestable_permission_id,
        target_user_id=target_user_id,
        note=note,
       # expiration_in_seconds=expiration_in_seconds,
    )
    print("Your request is in progress! 🏃🌴")
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