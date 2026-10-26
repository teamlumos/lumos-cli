import functools
import os

from click_extra import confirm, echo, prompt
from pick import pick

from lumos.common.client import AuthClient
from lumos.common.keyhelpers import key_file_path, read_key, write_key
from lumos.common.models import App, Permission, SupportRequestStatus


def authenticate(func):
    """Makes sure client is authenticated first.

    If LUMOS_CHECK_ONLY is set (see the `whoami --check` flag), this skips the
    interactive login flow entirely: it just verifies a credential is present
    on disk (or in the environment) and exits non-zero without prompting or
    opening a browser if it isn't. It does not verify the credential is still
    valid server-side; see the check_only handling in BaseClient._send_request
    for the case where a 401 comes back for a present-but-expired credential.
    """

    @functools.wraps(func)
    def wrapper_authenticate(*args, **kwargs):
        if os.environ.get("LUMOS_CHECK_ONLY"):
            if not os.environ.get("API_KEY") and not key_file_path().exists():
                echo("Not logged in.", err=True)
                raise SystemExit(1)
            read_key()
        else:
            setup(show_prompt=True)
        return func(*args, **kwargs)

    return wrapper_authenticate


def setup(show_prompt: bool = False, show_overwrite_prompt: bool = False):
    key_file = key_file_path()
    # if the key file exists, ask if they want to overwrite
    if key_file.exists():
        read_key()
        if not show_overwrite_prompt or not confirm(
            "You already have a key setup. Do you want to overwrite?", default=True
        ):
            return
    if show_prompt and not confirm(
        " 🛠️ You need to authenticate to use this application. Do you want to do that now?",
        default=True,
    ):
        raise SystemExit(1)
    selected, _ = pick(["OAuth 2.0", "API key"], "How do you want to authenticate?")
    if selected == "API key":
        echo(" ⚙️ Go to your Lumos account > Settings > API Tokens > Add an API Token, and copy the token.")
        api_key = prompt("API key", hide_input=True, confirmation_prompt=True)
        write_key(api_key)
    else:
        login()

    read_key()


def login(admin: bool | None = False):
    AuthClient().authenticate(admin or False)


def logout():
    key_file = key_file_path()
    key_file.unlink(missing_ok=True)
    if os.environ.get("API_KEY"):
        os.environ["API_KEY"] = None


def get_statuses(status: list[SupportRequestStatus], pending: bool, past: bool) -> set[SupportRequestStatus]:
    if not status:
        status = []
    if pending:
        status += SupportRequestStatus.PENDING_STATUSES
    if past:
        for e in SupportRequestStatus.ALL_STATUSES:
            if e in SupportRequestStatus.PENDING_STATUSES:
                continue
            status.append(e)

    if len(status) == 0:
        return None
    return set(status)


def check_current_apps(
    apps: list[App], selected_app: App, selected_permissions: list[Permission] | None
) -> tuple[App, str | None]:
    for app in apps:
        if str(app.app_id) == str(selected_app.id):
            if len(app.requestable_permissions) > 0 and selected_permissions:
                for permission in [str(r.id) for r in app.requestable_permissions]:
                    if permission in [str(r.id) for r in selected_permissions]:
                        return (
                            app,
                            "There's already a request for this app and permission",
                        )
            elif len(app.requestable_permissions) == 0 and not selected_permissions:
                return app, "There's already a request for this app"

    return None, None
