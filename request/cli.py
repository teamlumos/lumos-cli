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
            print(f"Selected app {app}\n")

        if not permission:
            # permission = typer.prompt("Enter the permission id")
            permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app)
            option, _ = pick(permissions, "Select a permission")
            permission = option.id
            print(f"Selected permission {permission}\n")

        create_access_request(app_id=app, note="", permission_id=permission, user_id=user, expiration=length)
        

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

def create_access_request(app_id, note, permission_id, user_id, expiration) -> List[App]:
    # TODO
    return []
    # apps: List[App] = client.create_access_request(
    #     app_id="67dfb94d-0292-e800-6ad3-459d94022a3e",
    #     permission_ids=[],
    #     target_user="",
    #     note="",
    #     expiration_in_seconds=15,
    # )
    # for app in apps:
    #     print(app)
    # return apps

@app.command()
def list_access_lengths(
    app: int,
    permission: int
) -> None:
    print(f"Listing access lengths for app {app} and permission {permission}")
    return

if __name__ == "__main__":
    app()