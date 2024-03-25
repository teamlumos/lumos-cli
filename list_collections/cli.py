from typing import Any, List, Optional, Tuple, Annotated
import typer
from uuid import UUID
from tabulate import tabulate

from common.client import Client
from common.models import App, Permission, SupportRequestStatus, User, AccessRequest

app = typer.Typer()

client = Client()

@app.command("users", help="List users in the system")
def list_users(
    like: Annotated[
        Optional[str],
        typer.Option(
            help="Search by name or email",
        ),
    ] = None,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    users, count, total = client.get_users(like=like, all=csv)
    display("users", [user.tabulate() for user in users], User.headers(), count, total, csv, id_only=id_only)


@app.command("permissions")
def list_permissions(
    app: UUID,
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters permissions")
    ] = None,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    permissions, count, total = client.get_app_requestable_permissions(app_id=app, search_term=like, all=csv)

    display("permissions", [permission.tabulate() for permission in permissions], Permission.headers(), count, total, csv, id_only=id_only)

@app.command("requests")
def list_requests(
    for_user: Annotated[
        Optional[UUID],
        typer.Option(help="Show only requests for ('targetting') a particular user")
    ] = None,
    mine: Annotated[
        bool,
        typer.Option(help="Show only requests for ('targetting') me. Takes precedence over --for-user.")
    ] = False,
    status: Annotated[
        Optional[List[str]],
        typer.Option(help="One of `PENDING`, `COMPLETED`, `DENIED_PROVISIONING`, etc",),
    ] = None,
    all_statuses: Annotated[
        bool,
        typer.Option(help="Show requests of all statuses (not just pending)")
    ] = False,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    
    if mine:
        for_user = client.get_current_user().id

    if all_statuses:
        status = None
    elif not status:
        status = SupportRequestStatus.PENDING_STATUSES

    access_requests, count, total, _, _ = client.get_access_requests(target_user_id=for_user, status=status, all=csv)

    rows = []
    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)
    for ar in access_requests:
        rows.append(ar.tabulate())

    display("requests", rows, AccessRequest.headers(), count, total, csv, id_only=id_only)

@app.command("apps")
def list_apps(
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters apps")
    ] = None,
    mine: Annotated[
        bool,
        typer.Option(help="Show only requests for ('targetting') me. Takes precedence over --for-user.")
    ] = False,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    if mine:
        user = client.get_current_user().id
        statuses = SupportRequestStatus.PENDING_STATUSES + SupportRequestStatus.SUCCESS_STATUSES
        access_requests, count, total, _, _ = client.get_access_requests(target_user_id=user, status=statuses, all=csv)
        print(tabulate([req.tabulate_as_app() for req in access_requests], headers=AccessRequest.headers()), "\n")
        return
    apps, count, total = client.get_appstore_apps(name_search=like, all=csv)
    display("apps", [app.tabulate() for app in apps], App.headers(), count, total, csv, id_only=id_only)

def display(description: str, tabular_data: List[List[Any]], headers: List[str], count: int, total: int, csv: bool, id_only: bool = False):
    if csv:
        for row in tabular_data:
            print(",".join([str(cell).replace(", ", "|") for cell in row]))
        return
    if id_only:
        if len(tabular_data) > 0:
            for row in tabular_data:
                print(row[0])
        return
    print(tabulate(tabular_data, headers=headers), "\n")
    if (count < total):
        print(f"There are {total - count} more {description} that match your search. Use --like to search.\n")