from typing import List, Optional
import typer
from uuid import UUID
from tabulate import tabulate
from pick import pick
import pytz

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

        create_access_request(app_id=app, requestable_permission_ids=selected_permissions, note=reason, expiration=length)
        
@app.command()
def list_permissions(
    app_id: str
) -> None:
    permissions: List[Permission] = client.get_app_requestable_permissions(app_id=app_id)
    print(tabulate([[permission.label, permission.id] for permission in permissions], headers=["Permission", "UUID"]), "\n")

@app.command()
def list() -> None:
    access_requests: List[AccessRequest] = client.get_access_requests()

    def convert_to_human_date(inp: str) -> str:
        import datetime

        # Parse the input UTC time string to a datetime object
        utc_time = datetime.datetime.strptime(inp, "%Y-%m-%dT%H:%M:%S")
        
        # Set the timezone to UTC for the parsed datetime
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        
        # Convert UTC time to EST
        est_time = utc_time.astimezone(pytz.timezone('America/New_York'))
        
        # Format the EST time into a more human-readable string
        human_date = est_time.strftime("%A, %B %d, %Y %I:%M %p EST")
        
        return human_date
    
    rows = []
    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)[:1]
    for ar in access_requests:
        rows.append(([ar.app_name, ar.status, convert_to_human_date(ar.requested_at), ar.supporter_user.email if ar.supporter_user else "Pending"]))

    print(tabulate(rows, headers=["App", "Request Status", "Requested At", "Approver Email"]), "\n")

@app.command()
def list_apps(
) -> None:
    apps: List[App] = client.get_appstore_apps()
    print(tabulate([[app.user_friendly_label, app.id] for app in apps], headers=["App", "UUID"]), "\n")

def create_access_request(
    app_id: UUID,
    requestable_permission_ids: List[UUID],
    note: str,
    expiration: Optional[int] = None
) -> None:
    client.create_access_request(
        app_id=str(app_id),
        permission_ids=[str(requestable_permission_id) for requestable_permission_id in requestable_permission_ids],
        note=note,
        # expiration_in_seconds=expiration,
    )
    print("Your request is in progress! 🏃🌴")

if __name__ == "__main__":
    app()