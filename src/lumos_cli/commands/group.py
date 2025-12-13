"""Group command group for Lumos CLI.

Commands:
    lumos group list - List groups in Lumos
"""

from uuid import UUID

from click_extra import group, option

from lumos_cli.commands.display import display
from lumos_cli.common.client import ApiClient
from lumos_cli.common.helpers import authenticate

client = ApiClient()


# Note: We use 'group_cmd' internally to avoid conflict with click's 'group' decorator
@group(name="group")
def group_cmd():
    """Manage groups."""
    pass


@group_cmd.command("list", help="List groups for the domain or the specified --app")
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


# Export with the expected name for CLI registration
group = group_cmd
