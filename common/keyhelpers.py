import os
from pathlib import Path
from common.logging import logdebug

def key_file_path() -> Path:
    if os.environ.get("DEV_MODE"):
        return Path.home() / ".lumos-dev"
    return Path.home() / ".lumos"
def write_key(key: str | None, scope: str | None = None) -> None:
    if not key:
        return
    if scope:
        key = f"{scope}:{key}"
    key_file = key_file_path()
    logdebug(f'Writing token [{key}] to {key_file}')
    with key_file.open("w") as f:
        f.write(key)

def read_key() -> str:
    api_key = os.environ.get("API_KEY")
    if api_key:
        return api_key
    
    key_file = key_file_path()
    with key_file.open("r") as f:
        api_key = f.read().strip()
    if api_key.count(":") == 1:
        scope, api_key = api_key.split(":")
        os.environ["SCOPE"] = scope
    os.environ["API_KEY"] = api_key
    return api_key