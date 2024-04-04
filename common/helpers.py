import functools
import os
from pathlib import Path
from common.client import AuthClient
import typer
from pick import pick

def authenticate(func):
    """Makes sure client is authenticated first"""
    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        setup(show_prompt=True)
        return func(*args, **kwargs)
    return wrapper_authenticate

def setup(show_prompt: bool = False, show_overwrite_prompt: bool = False):
    key_file = key_file_path()
    # if the key file exists, ask if they want to overwrite
    if key_file.exists():
        read_key()
        if not show_overwrite_prompt or not typer.confirm("You already have a key setup. Do you want to overwrite?", abort=False, default=True):
            return
    if show_prompt:
        typer.confirm(" 🛠️ You need to authenticate to use this application. Do you want to do that now?", abort=True, default=True)
    selected, _ = pick(["OAuth", "API key"], "How do you want to authenticate?")
    if selected == "API key":
        typer.echo(" ⚙️ Go to your Lumos account > Settings > API Tokens > Add an API Token, and copy the token.")
        api_key = typer.prompt("API key", hide_input=True)
        api_key_confirmation = typer.prompt("Confirm API key", hide_input=True)
        if (api_key != api_key_confirmation):
            typer.echo("API keys do not match.")
            raise typer.Exit(1)
        write_key(api_key)
    else:
        login()

    read_key()

def login(admin: bool = False):
    key = AuthClient().authenticate(admin)
    write_key(key)

def key_file_path() -> Path:
    if os.environ.get("DEV_MODE"):
        return Path.home() / ".lumos-dev"
    return Path.home() / ".lumos"

def write_key(key: str | None) -> None:
    if not key:
        return
    key_file = key_file_path()
    with key_file.open("w") as f:
        f.write(key)

def read_key() -> str:
    api_key = os.environ.get("API_KEY")
    if api_key:
        return api_key
    
    key_file = key_file_path()
    with key_file.open("r") as f:
        api_key = f.read().strip()
    os.environ["API_KEY"] = api_key
    return api_key