from typing import List
import typer
from appstore import __version__, __app_name__
import appstore

from appstore.client import Client, App, Permission

app = typer.Typer()

client = Client()

@app.command
def request(
    app: int = typer.Option(
        0,
        "--app",
        "-a",
        prompt="Enter the domain app id",
        help="The domain app id",
    ),
    user: int = typer.Option(
        0,
        "--user",
        "-u",
        prompt="Enter the user id",
        help="The user id",
    ),
    permission: int = typer.Option(
        0,
        "--permission",
        "-p",
        prompt="Enter the permission id",
        help="The permission id",
    ),
    length: int = typer.Option(
        0,
        "--length",
        "-l",
        prompt="Enter the access length",
        help="The length of time access is requested for",
    ),
) -> None:
    print(f"Requesting app {app}")

@app.command()
def list_apps() -> List[App]:
    apps: List[App] = client.get_appstore_apps()
    for app in apps:
        print(app)

@app.command()
def list_permissions() -> List[Permission]:
    permissions: List[Permission] = client.get_app_requestable_permissions(app_id="67dfb94d-0292-e800-6ad3-459d94022a3e")
    for permission in permissions:
        print(permission)

@app.command()
def create_access_request() -> List[App]:
    # TODO
    return
    # apps: List[App] = client.create_access_request(
    #     app_id="67dfb94d-0292-e800-6ad3-459d94022a3e",
    #     permission_ids=[],
    #     target_user="",
    #     note="",
    #     expiration_in_seconds=15,
    # )
    # for app in apps:
    #     print(app)
    # return apps

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
    return