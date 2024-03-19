from typing import Annotated, Optional
import typer
from lumos import __version__, __app_name__
import list_collections
import request
from pathlib import Path
from client import Client
import os
app = typer.Typer()

app.add_typer(request.app, name="request")
app.add_typer(list_collections.app, name="list")

client = Client()

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
    if (os.environ.get("DEV_MODE")):
        while not os.environ.get("API_KEY"):
            os.environ["API_KEY"] = typer.prompt("You are in dev mode, but you have not set an API key. Please set one now.")
        return
    
    key_file = Path.home() / ".lumos" 

    api_key: str | None = None
    if not key_file.exists():
        typer.echo("You need to save your API key to ~/.lumos to use this application.")
        typer.confirm("Do you want me to do that now?", abort=True, default=True)
        typer.echo("Go to your Lumos account > Settings > API Tokens > Add an API Token, and copy the token.")
        api_key = typer.prompt("API key", hide_input=True)
        api_key_confirmation = typer.prompt("Confirm API key", hide_input=True)
        if (api_key != api_key_confirmation):
            typer.echo("API keys do not match.")
            raise typer.Exit(1)
        with key_file.open("w") as f:
            f.write(api_key)
    else:
        with key_file.open("r") as f:
            api_key = f.read().strip()
    os.environ["API_KEY"] = api_key

@app.command("whoami")
def whoami(
    username: Annotated[
        Optional[bool],
        typer.Option(False, help="Show the username and exit"),
    ] = False,
) -> None:
    user = client.get_current_user()
    if username:
        typer.echo(user.email)
        return
    typer.echo(f"Logged in as {user.given_name} {user.family_name} ({user.email})")
    typer.echo(f"Your ID is {user.id}, if you need to reference it")