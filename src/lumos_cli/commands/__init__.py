"""Command modules for Lumos CLI.

This package contains noun-based command groups following RESTful CLI conventions:
- lumos app list
- lumos user list
- lumos group list
- lumos permission list
- lumos request create/list/status/poll/cancel
"""

from lumos_cli.commands.app import app
from lumos_cli.commands.group import group_cmd as group
from lumos_cli.commands.permission import permission
from lumos_cli.commands.request import request
from lumos_cli.commands.user import user

__all__ = ["app", "group", "permission", "request", "user"]
