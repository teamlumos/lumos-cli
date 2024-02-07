from typing import List, Optional
import typer
from uuid import UUID
from tabulate import tabulate
from pick import pick

from request.client import Client, App, Permission

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
            print("\n⏳ Loading your apps ...\n")
            apps: List[App] = client.get_appstore_apps()
            option, _ = pick(apps, "Select an app")
            app = option.id
            print(f"Selected app {app}")

        if not permission:
            print(f"\n⏳ Loading permissions for app {app} ...\n")
            permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app)
            if len(permissions) > 1:
                selected = pick(permissions, "Select a permission", multiselect=True, min_selection_count=1)
                selected_permissions = [option.id for option, _ in selected]
            elif len(permissions) == 1:
                selected_permissions = [permissions[0].id]
            print(f"Selected permissions: {selected_permissions}\n")
        
        if not reason:
            reason = typer.prompt("Enter your business justification for the request")

        create_access_request(app_id=app, requestable_permission_ids=selected_permissions, target_user_id=user, note=reason, expiration=length)
        

@app.command()
def list_permissions(
    app_id: str
) -> None:
    print(f"Listing permissions for app {app_id}\n")
    permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app_id)
    print(tabulate([[permission.label, permission.id] for permission in permissions], headers=["Permission", "UUID"]), "\n")

@app.command()
def list_apps(
) -> None:
    print("Listing all your apps...\n")
    apps: List[App] = client.get_appstore_apps()
    print(tabulate([[app.user_friendly_label, app.id] for app in apps], headers=["App", "UUID"]), "\n")

def create_access_request(
    app_id: str,
    requestable_permission_ids: List[UUID],
    target_user_id: str,
    note: str,
    expiration: Optional[int] = None
) -> None:
    client.create_access_request(
        app_id=str(app_id),
        permission_ids=[str(requestable_permission_id) for requestable_permission_id in requestable_permission_ids],
        target_user_id=str(target_user_id),
        note=note,
        # expiration_in_seconds=expiration,
    )
    print("Your request is in progress! 🏃🌴")

if __name__ == "__main__":
    app()