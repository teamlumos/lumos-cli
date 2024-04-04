from typing import Annotated, Optional
from common.helpers import authenticate, write_key, key_file_path, login as _login, setup as _setup, logout as _logout
import typer
from lumos import __version__, __app_name__
import list_collections
import request
from pathlib import Path
from common.client import ApiClient
import os
from pick import pick

app = typer.Typer()

app.add_typer(request.app, name="request")
app.add_typer(list_collections.app, name="list")

client = ApiClient()

def _version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v", help="Show the applications version and exit", callback=_version_callback, is_eager=True
    )
) -> None:
    pass

@app.command("whoami", help="Show information about the currently logged in user")
@authenticate
def whoami(
    username: Annotated[
        Optional[bool],
        typer.Option(help="Show the current user's username only")
    ] = False,
    id: Annotated[
        Optional[bool],
        typer.Option(help="Show the current user's ID only")
    ] = False,
) -> None:
    user = client.get_current_user()
    if username:
        typer.echo(user.email)
        return
    if id:
        typer.echo(user.id)
        return
    msg = f"Logged in as {user.given_name} {user.family_name} ({user.email})"
    if (scope := os.environ.get("SCOPE")):
        msg += f" as {scope}"
    typer.echo(msg)
    typer.echo(f"Your ID is {user.id}, if you need to reference it")

@app.command("setup", help="Setup your Lumos CLI. Can be used to login or change your authentication method.")
def setup():
    _setup(show_overwrite_prompt=True)

@app.command("login", help="Login to your Lumos account via OAuth.")
def login(
    admin: Annotated[
        Optional[bool],
        typer.Option(help="Log in as an admin, if you have the permission to do so")
    ] = False,):
    _logout()
    _login(admin)

@app.command("logout", help="Logout of your Lumos account.")
def logout():
    _logout()
    typer.echo(" 👋 Logged out!")
