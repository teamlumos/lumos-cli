"""User command group for Lumos CLI.

Commands:
    lumos user list - List users in Lumos
"""

from click_extra import group, option

from lumos_cli.commands.display import display
from lumos_cli.common.client import ApiClient
from lumos_cli.common.helpers import authenticate

client = ApiClient()


@group(name="user")
def user():
    """Manage users."""
    pass


@user.command("list", help="List users in Lumos")
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
