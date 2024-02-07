import typer
from appstore import __version__, __app_name__


app = typer.Typer()

@app.command()
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
    return

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