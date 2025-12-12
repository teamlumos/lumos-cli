import os

from colorama import Fore, Style


def logdebug_request(url, headers, body, params, method) -> None:
    logdebug(method + " " + url)
    headers_copy = headers.copy()
    if headers_copy.get("Authorization"):
        headers_copy["Authorization"] = headers_copy["Authorization"][:12] + "..."
    logdebug("HEADERS: " + str(headers_copy))
    logdebug("BODY: " + str(body))
    logdebug("PARAMETERS: " + str(params))


def logdebug_response(response) -> None:
    logdebug("\nRESPONSE: " + str(response.status_code))
    try:
        json = response.json()
        if json.get("access_token"):
            json["access_token"] = json["access_token"][:5] + "..."
        logdebug("HEADERS: " + str(response.headers))
        logdebug("CONTENT: " + str(json))
    except Exception:
        logdebug("CONTENT: " + str(response.content))


def logdebug(msg: str) -> None:
    if os.environ.get("DEBUG"):
        print(Fore.RED + msg)
        print(Style.RESET_ALL, end="\r")
