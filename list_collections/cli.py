from typing import List, Optional, Tuple, Annotated
import typer
from uuid import UUID
from tabulate import tabulate
from pick import pick
import pytz
from functools import reduce
import re

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
    print(tabulate([[user.id, user.given_name + " " + user.family_name, user.email] for user in users], headers=[ "ID", "Name", "Email"]), "\n")
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
    print(tabulate([[permission.id, permission.label, ", ".join(permission.duration_options)] for permission in permissions], headers=["ID", "Permission", "Access length options"]), "\n")
    if (len(permissions) < count):
        print(f"There are {count - len(permissions)} more permissions that match your search. Use --like to search.\n")

@app.command("requests")
def list_requests(
    app: Optional[UUID] = None,
    user: Optional[UUID] = None,
    mine: bool = False,
    status: Annotated[
        Optional[str],
        typer.Option(help="One of `PENDING`, `COMPLETED`, `DENIED_PROVISIONING`",),
    ] = None,
    inbound: bool = False,
) -> None:
    
    if mine:
        user = client.get_current_user().id

    access_requests, count = client.get_access_requests(target_user_id=user, app_id=app, status=status)

    def convert_to_human_date(inp: str) -> str:
        import datetime

        # Parse the input UTC time string to a datetime object
        utc_time = datetime.datetime.strptime(inp, "%Y-%m-%dT%H:%M:%S")
        
        # Set the timezone to UTC for the parsed datetime
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        
        # Convert UTC time to EST
        est_time = utc_time.astimezone(pytz.timezone('America/New_York'))
        
        # Format the EST time into a more human-readable string
        human_date = est_time.strftime("%a %b %d, %Y %I:%M %p EST")
        
        return human_date
    
    rows = []
    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)
    for ar in access_requests:
        rows.append([
            ar.app_name,
            ar.requester_user.given_name + " " + ar.requester_user.family_name,
            ar.target_user.given_name + " " + ar.target_user.family_name if ar.requester_user.id != ar.target_user.id else "",
            ar.status,
            convert_to_human_date(ar.requested_at),
            ar.supporter_user.email if ar.supporter_user else "Pending"])

    print(tabulate(rows, headers=["App", "Requested by", "Requested for", "Request Status", "Requested at", "Approver Email"]), "\n")
    if (len(access_requests) < count):
        print(f"There are {count - len(access_requests)} more requests. Filter by app or user.\n")

@app.command("apps")
def list_apps(
    like: Optional[str] = None
) -> None:
    apps, count = client.get_appstore_apps(name_search=like)
    print(tabulate([[app.user_friendly_label, app.id] for app in apps], headers=["ID", "App"]), "\n")
    if (len(apps) < count):
        print(f"There are {count - len(apps)} more apps that match your search. Use --like to search.\n")
