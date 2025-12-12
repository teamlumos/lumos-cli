import os

import requests
from click_extra import secho

from lumos_cli import __version__


def check_version_header(response: requests.Response) -> bool:
    if os.environ.get("WARNED"):
        return True
    if not (version_header_string := response.headers.get("X-CLI-Version")):
        return True

    current_version = parse_version(__version__)
    header_version = parse_version(version_header_string)
    cont, error_message = check_version(current_version, header_version)

    if error_message:
        secho(error_message, fg="cyan" if cont else "red")
    return cont


def check_version(current_version: list[int], header_version: list[int]) -> tuple[bool, str | None]:
    if current_version[0] < header_version[0]:
        return (
            False,
            "A new version of the CLI is available. Please run `brew upgrade lumos` to proceed.",
        )
    if current_version[0] == header_version[0] and current_version[1] < header_version[1]:
        os.environ["WARNED"] = "1"
        return (
            True,
            "There's an update available to the CLI. Please run `brew upgrade lumos`.",
        )
    return True, None


def parse_version(version: str) -> list[int]:
    return [int(v) for v in version.split(".")]
