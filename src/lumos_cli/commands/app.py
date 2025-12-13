"""App command group for Lumos CLI.

Commands:
    lumos app list - List apps in the appstore
"""

from click_extra import group, option
from tabulate import tabulate

from lumos_cli.commands.display import display
from lumos_cli.common.client import ApiClient
from lumos_cli.common.helpers import authenticate
from lumos_cli.common.models import AccessRequest

client = ApiClient()


@group(name="app")
def app():
    """Manage apps."""
    pass


@app.command("list", help="List apps in the appstore")
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
