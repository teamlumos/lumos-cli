from json import dumps
from uuid import UUID

from click_extra import group, option
from tabulate import tabulate

from lumos_cli.common.client import ApiClient
from lumos_cli.common.helpers import authenticate, get_statuses
from lumos_cli.common.models import AccessRequest, LumosModel

client = ApiClient()


@group(name="list")
def list_group():
    """List various Lumos resources"""
    pass


@list_group.command("users", help="List users in Lumos")
@option("--like", default=None, help="Search by name or email")
@option("--csv", is_flag=True, help="Output as CSV")
@option("--json", "output_json", is_flag=True, help="Output as JSON")
@option("--paginate/--no-paginate", default=True, help="Pagination")
@option("--page-size", default=100, help="Page size")
@option("--page", default=1, help="Page")
@option("--id-only", is_flag=True, help="Output ID only")
@authenticate
def list_users(
    like: str | None,
    csv: bool,
    output_json: bool,
    paginate: bool,
    page_size: int,
    page: int,
    id_only: bool,
) -> None:
    all = csv or output_json or not paginate
    users, count, total = client.get_users(like=like, all=all, page=page, page_size=page_size)
    display(
        "users",
        users,
        count,
        total,
        csv,
        output_json,
        page=page,
        page_size=page_size,
        id_only=id_only,
    )


@list_group.command("permissions", help="List permissions for a given app")
@option("--app", required=True, type=str, help="App UUID")
@option("--like", default=None, help="Filters permissions")
@option("--csv", is_flag=True, help="Output as CSV")
@option("--json", "output_json", is_flag=True, help="Output as JSON")
@option("--paginate/--no-paginate", default=True, help="Pagination")
@option("--page-size", default=100, help="Page size")
@option("--page", default=1, help="Page")
@option("--id-only", is_flag=True, help="Output ID only")
@authenticate
def list_permissions(
    app: str,
    like: str | None,
    csv: bool,
    output_json: bool,
    paginate: bool,
    page_size: int,
    page: int,
    id_only: bool,
) -> None:
    app_uuid = UUID(app)
    all = csv or output_json or not paginate
    permissions, count, total = client.get_app_requestable_permissions(
        app_id=app_uuid, search_term=like, all=all, page=page, page_size=page_size
    )

    display(
        "permissions",
        permissions,
        count,
        total,
        csv,
        output_json,
        page=page,
        page_size=page_size,
        id_only=id_only,
    )


@list_group.command("groups", help="List groups for the domain or the specified --app")
@option(
    "--app",
    default=None,
    type=str,
    help="App ID to filter groups by. If not provided, lists all groups.",
)
@option("--like", default=None, help="Filters groups")
@option("--csv", is_flag=True, help="Output as CSV")
@option("--json", "output_json", is_flag=True, help="Output as JSON")
@option("--paginate/--no-paginate", default=True, help="Pagination")
@option("--page-size", default=100, help="Page size")
@option("--page", default=1, help="Page")
@option("--id-only", is_flag=True, help="Output ID only")
@authenticate
def list_groups(
    app: str | None,
    like: str | None,
    csv: bool,
    output_json: bool,
    paginate: bool,
    page_size: int,
    page: int,
    id_only: bool,
) -> None:
    app_uuid = UUID(app) if app else None
    all = csv or output_json or not paginate
    groups, count, total = client.get_groups(app_id=app_uuid, search_term=like, all=all, page=page, page_size=page_size)

    display(
        "groups",
        groups,
        count,
        total,
        csv,
        output_json,
        page=page,
        page_size=page_size,
        id_only=id_only,
    )


@list_group.command("requests", help="List access requests")
@option(
    "--for-user",
    default=None,
    type=str,
    help="Show only requests for ('targetting') a particular user",
)
@option(
    "--mine",
    is_flag=True,
    help="Show only requests for ('targetting') me. Takes precedence over --for-user.",
)
@option(
    "--status",
    multiple=True,
    help="One of `PENDING`, `COMPLETED`, `DENIED_PROVISIONING`, etc",
)
@option("--pending", is_flag=True, help="Show only pending requests")
@option("--past", is_flag=True, help="Show only past requests")
@option("--csv", is_flag=True, help="Output as CSV")
@option("--json", "output_json", is_flag=True, help="Output as JSON")
@option("--paginate/--no-paginate", default=True, help="Pagination")
@option("--page-size", default=100, help="Page size")
@option("--page", default=1, help="Page")
@option("--id-only", is_flag=True, help="Output ID only")
@authenticate
def list_requests(
    for_user: str | None,
    mine: bool,
    status: tuple,
    pending: bool,
    past: bool,
    csv: bool,
    output_json: bool,
    paginate: bool,
    page_size: int,
    page: int,
    id_only: bool,
) -> None:
    user_uuid = None
    if mine:
        user_uuid = client.get_current_user_id()
    elif for_user:
        user_uuid = UUID(for_user)

    status_list = list(status) if status else None
    status_set = get_statuses(status_list, pending, past)

    all = csv or output_json or not paginate
    access_requests, count, total, _, _ = client.get_access_requests(
        target_user_id=user_uuid,
        status=status_set,
        all=all,
        page=page,
        page_size=page_size,
    )

    access_requests = sorted(access_requests, key=lambda x: x.requested_at, reverse=True)

    display(
        "requests",
        access_requests,
        count,
        total,
        csv,
        output_json,
        page_size=page_size,
        page=page,
        id_only=id_only,
        search=False,
    )


@list_group.command("apps", help="List apps in the appstore")
@option("--like", default=None, help="Filters apps by search term")
@option("--mine", is_flag=True, help="Show only my apps.")
@option("--csv", is_flag=True, help="Output as CSV")
@option("--json", "output_json", is_flag=True, help="Output as JSON")
@option("--paginate/--no-paginate", default=True, help="Pagination")
@option("--page-size", default=100, help="Page size")
@option("--page", default=1, help="Page")
@option("--id-only", is_flag=True, help="Output ID only")
@authenticate
def list_apps(
    like: str | None,
    mine: bool,
    csv: bool,
    output_json: bool,
    paginate: bool,
    page_size: int,
    page: int,
    id_only: bool,
) -> None:
    all = csv or output_json or not paginate
    if mine:
        access_requests = client.get_my_apps()
        if len(access_requests) > 0:
            print(
                tabulate(
                    [req.tabulate_as_app() for req in access_requests],
                    headers=AccessRequest.headers(),
                ),
                "\n",
            )
        else:
            print("No apps found.")
        return
    apps, count, total = client.get_appstore_apps(name_search=like, all=all, page_size=page_size, page=page)
    display(
        "apps",
        apps,
        count,
        total,
        csv,
        output_json,
        page=page,
        page_size=page_size,
        id_only=id_only,
    )


def display(
    description: str,
    data: list[LumosModel],
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
    if remaining > 0:
        if search:
            print(f"There are {remaining} more {description} that match your search. Use --like to search.\n")
        else:
            print(f"There are {remaining} more {description} not shown.\n")
