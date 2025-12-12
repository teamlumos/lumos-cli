import os

from requests import Response

from lumos_cli import __version__
from lumos_cli.common.client_helpers import check_version_header, parse_version


def test_parse_version():
    assert parse_version("1.2.3") == [1, 2, 3]


def test_check_version_header_no_version():
    response = Response()
    assert check_version_header(response) is True


def test_check_version_header_same_version():
    response = Response()
    response.headers["X-CLI-Version"] = __version__

    assert check_version_header(response) is True


def test_check_version_header_lower_version():
    response = Response()
    response.headers["X-CLI-Version"] = "1.1.1"
    assert check_version_header(response) is True


def test_check_version_header_higher_version():
    current_version = parse_version(__version__)
    current_version[0] += 1
    response = Response()
    response.headers["X-CLI-Version"] = f"{current_version[0] + 1}.0.0"

    assert check_version_header(response) is False


def test_check_version_header_higher_version_already_warned():
    os.environ["WARNED"] = "1"
    current_version = parse_version(__version__)
    current_version[0] += 1
    response = Response()
    response.headers["X-CLI-Version"] = f"{current_version[0] + 1}.0.0"

    assert check_version_header(response) is True
    os.environ.pop("WARNED")
