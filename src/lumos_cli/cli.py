import os

from click_extra import Context, echo, group, option, pass_context

from lumos_cli.common.client import ApiClient
from lumos_cli.common.helpers import authenticate
from lumos_cli.common.helpers import login as _login
from lumos_cli.common.helpers import logout as _logout
from lumos_cli.common.helpers import setup as _setup
from lumos_cli.common.logging import logdebug

client = ApiClient()


@group(
    context_settings={"help_option_names": ["-h", "--help"]},
)
@option("--debug", is_flag=True, help="Enable debug mode", hidden=True)
@pass_context
def lumos(ctx: Context, debug: bool) -> None:
    """Lumos CLI - Command line interface for Lumos"""
    if debug:
        os.environ["DEBUG"] = "1"
        logdebug("🐞 Debug mode enabled")


@lumos.command("whoami", help="Show information about the currently logged in user.")
@option("--username", is_flag=True, help="Show the current user's username only")
@option("--id", "show_id", is_flag=True, help="Show the current user's ID only")
@authenticate
def whoami(username: bool, show_id: bool) -> None:
    user = client.get_current_user()
    if username:
        echo(user.email)
        return
    if show_id:
        echo(user.id)
        return
    msg = f" 💻 Logged in as {user.given_name} {user.family_name} ({user.email})"
    if scope := os.environ.get("SCOPE"):
        msg += f" as {scope}"
    echo(msg)
    echo(f"Your ID is {user.id}, if you need to reference it")


@lumos.command(
    "setup",
    help="Setup your Lumos CLI. Can be used to login or change your authentication method.",
)
def setup():
    _setup(show_overwrite_prompt=True)
    # Call whoami command programmatically
    ctx = Context(whoami)
    ctx.invoke(whoami, username=False, show_id=False)


@lumos.command(
    "login",
    help="Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.",
)
@option(
    "--admin",
    is_flag=True,
    help="Log in as an admin, if you have the permission to do so",
)
def login(admin: bool):
    _logout()
    _login(admin)
    # Call whoami command programmatically
    ctx = Context(whoami)
    ctx.invoke(whoami, username=False, show_id=False)


@lumos.command("logout", help="Logout of your Lumos account.")
def logout():
    _logout()
    echo(" 👋 Logged out!")


# Import and register subcommands
def register_subcommands():
    """Register all subcommands after the main CLI group is defined"""
    # Import new noun-based command groups
    from lumos_cli.commands import app, group, permission, request, user

    # Register new RESTful command structure (lumos <noun> <verb>)
    lumos.add_command(app)
    lumos.add_command(user)
    lumos.add_command(group)
    lumos.add_command(permission)
    lumos.add_command(request)


# Register subcommands at module load time
register_subcommands()

if __name__ == "__main__":
    lumos()
