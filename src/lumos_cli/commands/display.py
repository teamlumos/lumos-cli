"""Shared display utilities for CLI output formatting."""

from json import dumps

from tabulate import tabulate

from lumos_cli.common.models import LumosModel


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
    """Display a list of Lumos models in various formats.

    Args:
        description: Name of the resource type (e.g., "users", "apps")
        data: List of model objects to display
        count: Number of items in current page
        total: Total number of items available
        csv: Output as CSV format
        json: Output as JSON format
        page: Current page number
        page_size: Number of items per page
        id_only: Output only IDs
        search: Whether to show search hint for remaining items
    """
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
