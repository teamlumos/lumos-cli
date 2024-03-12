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
    local_api_key = os.environ.get("API_KEY")
    if local_api_key:
        os.environ["API_KEY"] = local_api_key
        typer.echo("****************************************")
        typer.echo("Using API key from environment variable.")
        typer.echo("****************************************")
        return
    key_file = Path.home() / ".lumos" 

    if not key_file.exists():
        typer.echo("You need to save your API key to ~/.lumos to use this application. (y/n)")
        typer.confirm("Do you want me to do that now?", abort=True, default=True)
        api_key = typer.prompt("Please paste your API key")
        with key_file.open("w") as f:
            f.write(api_key)
    else:
        with key_file.open("r") as f:
            os.environ["API_KEY"] = f.read().strip()

@app.command("whoami")
def whoami() -> None:
    user = client.get_current_user()
    typer.echo(f"Logged in as {user.given_name} {user.family_name} ({user.email})")
    typer.echo(f"Your ID is {user.id}, if you need to reference it")