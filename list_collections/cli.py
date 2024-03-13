from typing import List, Optional, Tuple, Annotated
import typer
from uuid import UUID
from tabulate import tabulate

from client import Client
from models import App, Permission, SupportRequestStatus, User, AccessRequest

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
    users, count = client.get_users(like=like)
    print(tabulate([user.tabulate() for user in users], headers=User.headers()), "\n")
    if (len(users) < count):
        print(f"There are {users - len(users)} more users that match your search. Use --like to search.\n")


@app.command("permissions")
def list_permissions(
    app: UUID,
    like: Optional[str] = None,
    user: Optional[UUID] = None,
    mine: bool = False,
) -> None:
    permissions, count = client.get_app_requestable_permissions(app_id=app, search_term=like)
    print(tabulate([permission.tabulate() for permission in permissions], headers=Permission.headers()), "\n")
    if (len(permissions) < count):
        print(f"There are {count - len(permissions)} more permissions that match your search. Use --like to search.\n")

@app.command("requests")
def list_requests(
    app: Optional[UUID] = None,
    user: Optional[UUID] = None,
    mine: bool = False,
    status: Annotated[
        Optional[List[str]],
        typer.Option(help="One of `PENDING`, `COMPLETED`, `DENIED_PROVISIONING`, etc",),
    ] = None,
    all_statuses: bool = False,
) -> None:
    
    if mine:
        user = client.get_current_user().id

    if all_statuses:
        status = None
    elif not status:
        status = SupportRequestStatus.PENDING_STATUSES

    access_requests, count = client.get_access_requests(target_user_id=user, app_id=app, status=status)

    rows = []
    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)
    for ar in access_requests:
        rows.append(ar.tabulate())

    print(tabulate(rows, headers=AccessRequest.headers()), "\n")
    if (len(access_requests) < count):
        print(f"There are {count - len(access_requests)} more requests. Filter by app or user.\n")

@app.command("apps")
def list_apps(
    like: Optional[str] = None
) -> None:
    apps, count = client.get_appstore_apps(name_search=like)
    print(tabulate([app.tabulate() for app in apps], headers=App.headers()), "\n")
    if (len(apps) < count):
        print(f"There are {count - len(apps)} more apps that match your search. Use --like to search.\n")
