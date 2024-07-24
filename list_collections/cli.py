from typing import Any, List, Optional, Annotated
from common.helpers import authenticate, get_statuses
import typer
from uuid import UUID
from tabulate import tabulate
from json import dumps

from common.client import ApiClient
from common.models import AccessRequest, LumosModel, SupportRequestStatus

app = typer.Typer()

client = ApiClient()

@app.command("users", help="List users in Lumos")
@authenticate
def list_users(
    like: Annotated[
        Optional[str],
        typer.Option(
            help="Search by name or email",
        ),
    ] = None,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    json: Annotated[bool, typer.Option(help="Output as JSON")] = False,
    paginate: Annotated[bool, typer.Option(help="Pagination")] = True,
    page_size: Annotated[int, typer.Option(help="Page size")] = 100,
    page: Annotated[int, typer.Option(help="Page")] = 1,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    all=csv or json or not paginate
    users, count, total = client.get_users(like=like, all=all, page=page, page_size=page_size)
    display("users", users, count, total, csv, json, page=page, page_size=page_size, id_only=id_only)


@app.command("permissions", help="List permissions for a given app")
@authenticate
def list_permissions(
    app: UUID,
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters permissions")
    ] = None,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    json: Annotated[bool, typer.Option(help="Output as JSON")] = False,
    paginate: Annotated[bool, typer.Option(help="Pagination")] = True,
    page_size: Annotated[int, typer.Option(help="Page size")] = 100,
    page: Annotated[int, typer.Option(help="Page")] = 1,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    all=csv or json or not paginate
    permissions, count, total = client.get_app_requestable_permissions(app_id=app, search_term=like, all=all, page=page, page_size=page_size)

    display("permissions", permissions, count, total, csv, json, page=page, page_size=page_size, id_only=id_only)

@app.command("groups", help="List groups for the domain or the specified --app")
@authenticate
def list_groups(
    app: Annotated[
        Optional[UUID],
        typer.Option(help="App ID to filter groups by. If not provided, lists all groups.")
    ]= None,
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters groups")
    ] = None,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    json: Annotated[bool, typer.Option(help="Output as JSON")] = False,
    paginate: Annotated[bool, typer.Option(help="Pagination")] = True,
    page_size: Annotated[int, typer.Option(help="Page size")] = 100,
    page: Annotated[int, typer.Option(help="Page")] = 1,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    all=csv or json or not paginate
    groups, count, total = client.get_groups(app_id=app, search_term=like, all=all, page=page, page_size=page_size)

    display("groups", groups, count, total, csv, json, page=page, page_size=page_size, id_only=id_only)

@app.command("requests", help="List access requests")
@authenticate
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
    pending: Annotated[bool, typer.Option(help="Show only pending requests")] = False,
    past: Annotated[bool, typer.Option(help="Show only past requests")] = False,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    json: Annotated[bool, typer.Option(help="Output as JSON")] = False,
    paginate: Annotated[bool, typer.Option(help="Pagination")] = True,
    page_size: Annotated[int, typer.Option(help="Page size")] = 100,
    page: Annotated[int, typer.Option(help="Page")] = 1,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    
    if mine:
        for_user = client.get_current_user_id()

    status = get_statuses(status, pending, past)

    all=csv or json or not paginate
    access_requests, count, total, _, _ = client.get_access_requests(
        target_user_id=for_user,
        status=status,
        all=all,
        page=page, 
        page_size=page_size
    )

    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)

    display("requests",
        access_requests,
        count,
        total,
        csv,
        json,
        page_size=page_size,
        page=page,
        id_only=id_only,
        search=False)

@app.command("apps", help="List apps in the appstore")
@authenticate
def list_apps(
    like: Annotated[
        Optional[str],
        typer.Option(help="Filters apps by search term")
    ] = None,
    mine: Annotated[
        bool,
        typer.Option(help="Show only my apps.")
    ] = False,
    csv: Annotated[bool, typer.Option(help="Output as CSV")] = False,
    json: Annotated[bool, typer.Option(help="Output as JSON")] = False,
    paginate: Annotated[bool, typer.Option(help="Pagination")] = True,
    page_size: Annotated[int, typer.Option(help="Page size")] = 100,
    page: Annotated[int, typer.Option(help="Page")] = 1,
    id_only: Annotated[bool, typer.Option(help="Output ID only")] = False,
) -> None:
    all=csv or json or not paginate
    if mine:
        access_requests = client.get_my_apps()
        if len(access_requests) > 0:
            print(tabulate([req.tabulate_as_app() for req in access_requests], headers=AccessRequest.headers()), "\n")
        else:
            print("No apps found.")
        return
    apps, count, total = client.get_appstore_apps(name_search=like,
        all=all,
        page_size=page_size,
        page=page)
    display("apps", apps, count, total, csv, json, page=page, page_size=page_size, id_only=id_only)

def display(description: str,
    data: List[LumosModel],
    count: int,
    total: int,
    csv: bool,
    json: bool,
    page: int,
    page_size: int,
    id_only: bool = False,
    search: bool = True,
):
    if len(data) == 0:
        print(f"No {description} found.")
        return
    if csv:
        for row in data:
            print(",".join([str(cell).replace(", ", "|") for cell in row.tabulate()]))
        return
    if json:
        print(dumps([d.__dict__ for d in data], default=str, indent=2))
        return
    if id_only:
        if len(data) > 0:
            for row in data:
                print(row.tabulate()[0])
        return
    headers = data[0].headers()
    print(tabulate([d.tabulate() for d in data], headers=headers), "\n")
    remaining = total - count - page_size * (page - 1)
    if (remaining > 0):
        if search:
            print(f"There are {remaining} more {description} that match your search. Use --like to search.\n")
        else:
            print(f"There are {remaining} more {description} not shown.\n")
