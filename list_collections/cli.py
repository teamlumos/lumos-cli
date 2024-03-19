from typing import List, Optional, Tuple, Annotated
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
    ] = None
) -> None:
    users, count, total = client.get_users(like=like)
    print(tabulate([user.tabulate() for user in users], headers=User.headers()), "\n")
    if (count < total):
        print(f"There are {total - count} more users that match your search. Use --like to search.\n")


@app.command("permissions")
def list_permissions(
    app: UUID,
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters permissions")
     ] = None,
) -> None:
    permissions, count, total = client.get_app_requestable_permissions(app_id=app, search_term=like)
    print(tabulate([permission.tabulate() for permission in permissions], headers=Permission.headers()), "\n")
    if (count < total):
        print(f"There are {total - count} more permissions that match your search. Use --like to search.\n")

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
) -> None:
    
    if mine:
        for_user = client.get_current_user().id

    if all_statuses:
        status = None
    elif not status:
        status = SupportRequestStatus.PENDING_STATUSES

    access_requests, count, total, _, _ = client.get_access_requests(target_user_id=for_user, status=status)

    rows = []
    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)
    for ar in access_requests:
        rows.append(ar.tabulate())

    print(tabulate(rows, headers=AccessRequest.headers()), "\n")
    if (total < total):
        print(f"There are {total - count} more requests. Filter by app or user.\n")

@app.command("apps")
def list_apps(
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters apps")
    ] = None,
    mine: Annotated[
        bool,
        typer.Option(help="Show only requests for ('targetting') me. Takes precedence over --for-user.")
     ] = False) -> None:
    if mine:
        user = client.get_current_user().id
        statuses = SupportRequestStatus.PENDING_STATUSES + SupportRequestStatus.SUCCESS_STATUSES
        access_requests, count, total, _, _ = client.get_access_requests(target_user_id=user, status=statuses)
        print(tabulate([req.tabulate_as_app() for req in access_requests], headers=AccessRequest.headers()), "\n")
        return
    apps, count, total = client.get_appstore_apps(name_search=like)
    print(tabulate([app.tabulate() for app in apps], headers=App.headers()), "\n")
    if (count < total):
        print(f"There are {total - count} more apps that match your search. Use --like to search.\n")
