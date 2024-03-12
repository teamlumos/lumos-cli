from typing import List, Optional, Tuple, Annotated
import typer
from uuid import UUID
from tabulate import tabulate
import os
from client import Client
from models import App, Permission, User, AccessRequest

app = typer.Typer()

client = Client()

@app.callback(invoke_without_command=True)
def status(
    request_id: Annotated[
        Optional[str],
        typer.Option(
            help="Request ID",
        ),
    ] = None,
    last: bool = False
) -> None:
    if last:
        client.get_current_user()
        access_requests, count = client.get_access_requests(target_user_id=UUID(os.environ["USER_ID"]))
        if count == 0:
            typer.echo("No pending requests found")
            return
        request_id = access_requests[0].id
    if not request_id:
        request_id = typer.prompt("Please provide a request ID")
    request = client.get_request_status(request_id)
    print(tabulate([request.tabulate()], headers=AccessRequest.headers()), "\n")
