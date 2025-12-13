"""Permission command group for Lumos CLI.

Commands:
    lumos permission list - List permissions for a given app
"""

from uuid import UUID

from click_extra import group, option

from lumos_cli.commands.display import display
from lumos_cli.common.client import ApiClient
from lumos_cli.common.helpers import authenticate

client = ApiClient()


@group(name="permission")
def permission():
    """Manage permissions."""
    pass


@permission.command("list", help="List permissions for a given app")
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
