
from abc import abstractmethod
import time
from typing import Any, Dict, Tuple
import requests
from lumos import __version__
from common.models import App, AccessRequest, Permission, User
from uuid import UUID
from typing import Any, Dict, List, Optional
from common.models import App, AccessRequest, Permission, User
from common.logging import logdebug, logdebug_request, logdebug_response
import os
import typer
from common.keyhelpers import write_key
import webbrowser

class BaseClient:
    url: str

    def __init__(self, url: str):
        self.url = url
    
    def get(self, endpoint: str, params: dict = {}):
        """Function to call an API endpoint and return the response."""
        return self._send_request("GET", endpoint, params=params)
    
    def get_paged(
        self,
        endpoint: str, 
        params: dict = {}
    ) -> Tuple[List[dict[str, Any]], int, int, int, int]:
        """Function to call an API endpoint and return the paged response."""
        response = self.get(endpoint, params=params)
        if response:
            return response["items"], len(response["items"]), int(response["total"]), int(response["page"]), int(response["pages"])
        return [], 0, 0, 0, 0
    
    def get_all(self,
        endpoint: str,
        params: dict = {}
    ) -> Tuple[List[dict[str, Any]], int, int, int, int]:
        """Function to call an API endpoint and return all the results."""
        all_results = []
        page = 1
        while True:
            results, _, _, _, pages = self.get_paged(endpoint, params={**params, "page": page, "size": 100})
            all_results.extend(results)
            if page == pages:
                break
            page += 1
        count = len(all_results)
        return all_results, count, count, 1, 1
    
    def get_all_or_paged(self,
        endpoint: str,
        params: dict = {},
        all: bool = False
    ) -> Tuple[List[dict[str, Any]], int, int, int, int]:
        """Function to call an API endpoint and return all the results."""
        if all:
            return self.get_all(endpoint, params=params)
        return self.get_paged(endpoint, params=params)

    def post(self, endpoint: str, body: Dict[str, Any]):
        """Function to call an API endpoint and return the response."""
        return self._send_request("POST", endpoint, body=body)
    
    def _send_request(self,
        method: str,
        endpoint: str,
        body: dict | None = None,
        params: dict = {},
        retry: int = 0,
    ):
        if retry > 3:
            typer.echo("Too many retries. Exiting.", err=True)
            raise typer.Exit(1)
        url, headers = self._get_url_and_headers(endpoint)
        logdebug_request(url, headers, body, params, method)

        response = requests.request(method, url, headers=headers, json=body, params=params)
        logdebug_response(response)

        if response.ok:
            return response.json()
        if response.status_code == 429:
            typer.echo("We're being rate limited. Waiting a sec.", err=True)
            retry += 1
            time.sleep(retry)
            return self._send_request(method, endpoint, body, params, retry)
        if response.status_code == 401:
            if retry > 1 or not (scope := os.environ.get("SCOPE")):
                typer.echo("Something went wrong with authorization. Try logging in again.", err=True)
                raise typer.Exit(1)
            typer.echo("Something went wrong with authorization. Trying to log in again.", err=True)
            AuthClient().authenticate(scope == "admin")
            return self._send_request(method, endpoint, body, params, retry + 1)
        elif response.status_code == 403:
            typer.echo("You don't have permission to do that.", err=True)
        else:
            typer.echo(f"An error occurred (status code {response.status_code}). Check the IDs provided--they may not exist.", err=True)
        raise typer.Exit(1)

    @abstractmethod
    def _get_url_and_headers(self, endpoint: str) -> tuple[str, dict[str, str]]:
        pass
    
class AuthClient(BaseClient):
    GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
    HEADERS = {
        "content-type": "application/x-www-form-urlencoded",
        "User-Agent": f"lumos-cli/{__version__}",
    }

    def __init__(self):
        auth_url: str | None = None
        if (os.environ.get("DEV_MODE")):
            auth_url = os.environ.get("AUTH_URL")
        super().__init__(auth_url or "https://b.app.lumosidentity.com")
    
    def _get_url_and_headers(self, endpoint: str) -> tuple[str, dict[str, str]]:
        return f"{self.url}/b/oauth/{endpoint}", self.HEADERS
    
    def _get_client_id(self) -> str:
        if (auth_url := os.environ.get("AUTH_URL")):
            if "localhost" in auth_url:
                return "IHcwQtVXJH8RVrPag3Tqi17KDdI6X9Ja"
            if "qa" in auth_url:
                return "37o8paGpj1BvV6NOFmVO21cG8L9ePSCs"
            if "staging" in auth_url:
                return "tLPbUcyJZZyEvuxTo5deyFQXkO9iXZyx"
        return "XfsajAwB6pl2XyNYwzrVkTI15ISbQ2dR"
    
    def authenticate(self, admin: bool = False):
        url, headers = self._get_url_and_headers("device/code")
        client_id = self._get_client_id()
        scope = "admin" if admin else "user"
        params = {
            "client_id": client_id,
            "scope": scope,
        }
        logdebug_request(url, headers, None, params, 'POST')

        response = requests.post(url, headers=headers, params=params)
        if not response.ok:
            typer.echo(f"Something went wrong.")
            logdebug_response(response)
            raise typer.Exit(1)
        
        device_auth_data = response.json()

        verification_uri_complete = device_auth_data["verification_uri_complete"]
        if (os.environ.get("DEV_MODE")):
            if (url.startswith("http://")):
                verification_uri_complete = verification_uri_complete.replace("https://", "http://")
            if ("localhost:3000" in verification_uri_complete):
                verification_uri_complete = verification_uri_complete.replace("localhost:3000", "localhost:8080")
        
        webbrowser.open(verification_uri_complete)

        token_data = {
            "client_id": client_id,
            "device_code": device_auth_data["device_code"],
            "grant_type": self.GRANT_TYPE,
        }
        token_url, _ = self._get_url_and_headers("token")
        typer.echo(f" 🔑 Please go to {verification_uri_complete} to authenticate. You must already be logged in to Lumos on your browser.")

        logdebug_request(token_url, headers, token_data, None, 'POST')

        wait = 0
        while True:
            print(" ⏰ Waiting" + ("." * (wait % 10)) + (' ' * (10-(wait % 10))), end='\r')
            token_response = requests.post(token_url, headers=headers, data=token_data)
            if token_response.status_code == 400:
                typer.echo(f"Bad request: {token_response.json()}")
                raise typer.Exit(1)
            logdebug_response(token_response)
            if token_response.status_code != 200:
                time.sleep(1)
                wait += 1
            else:
                token_data = token_response.json()
                token = token_data["access_token"]
                break
            if wait > 60:
                typer.echo("Timed out waiting for authentication.")
                raise typer.Exit(1)
        typer.echo(" ✅ Authenticated!")
        write_key(token, scope)
    
class ApiClient(BaseClient):
    def __init__(self):
        api_url: str | None = None
        if (os.environ.get("DEV_MODE")):
            api_url = os.environ.get("API_URL")
        super().__init__(api_url or "https://api.lumos.com")

    def _get_url_and_headers(self, endpoint: str) -> Tuple[str, Dict[str, str]]:
        api_key = os.environ.get("API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": f"lumos-cli/{__version__}",
        }
        return f"{self.url}/{endpoint}", headers
    
    def get_current_user_id(self) -> UUID:
        if not os.environ.get("USER_ID"):
            user = self.get_current_user()
            os.environ["USER_ID"] = str(user.id)
            return user.id
        return UUID(os.environ["USER_ID"])
    
    def get_current_user(self) -> User:
        user = self.get("users/current")
        if user:
            os.environ["USER_ID"] = user["id"]
            return User(**user)
        typer.echo("You are not logged in", err=True)
        raise typer.Exit(1)

    def get_appstore_app(self, id: UUID) -> App | None:
        raw_app = self.get(f"appstore/apps/{id}")
        if raw_app:
            return App(**raw_app)
        return None
    
    def get_request_status(self, id: UUID) -> AccessRequest | None:
        raw_request = self.get(f"appstore/access_requests/{id}")
        return self._create_access_request(raw_request)
    
    def _create_access_request(self, raw_request: dict | None) -> AccessRequest | None:
        if not raw_request:
            return None
        return AccessRequest(**raw_request)
    
    def get_appstore_apps(self, name_search: str | None = None, all: bool =False) -> Tuple[List[App], int, int]:
        endpoint = "appstore/apps"
        params: dict[str, Any] = {}
        if name_search:
            params["name_search"] = name_search
        raw_apps, count, total, _, _ = self.get_all_or_paged(endpoint, params=params, all=all)
        apps: List[App] = []
        for item in raw_apps:
            apps.append(App(**item))
        return apps, count, total
    
    def get_access_requests(
        self,
        app_id: UUID | None = None,
        target_user_id: UUID | None = None,
        status: List[str] | None = None,
        page: int = 1,
        count: int = 25,
        all: bool = False
    ) -> Tuple[List[AccessRequest], int, int, int, int]:
        params: dict[str, Any]= {
            "size": count
        }
        if target_user_id:
            params["target_user_id"] = str(target_user_id)
        if (status and len(status) > 0):
            params["statuses"] = [str(s) for s in status]

        endpoint = "appstore/access_requests"
        raw_access_requests, count, total, page, pages = self.get_all_or_paged(endpoint, params=params, all=all)
        access_requests: List[AccessRequest] = []
        for item in raw_access_requests:
            access_request = self._create_access_request(item)
            if (access_request): 
                access_requests.append(access_request)
        return sorted(access_requests, key=lambda x: x.requested_at, reverse=True), count, total, page, pages
    
    def get_users(self, like: Optional[str] = None, all: bool = False) -> Tuple[List[User], int, int]:
        endpoint = "users"
        params: dict[str, Any] = {}
        if like:
            params["search_term"] = like
        raw_users, count, total, _, _ = self.get_all_or_paged(endpoint, params=params, all=all)

        users: List[User] = []
        for item in raw_users:
            users.append(User(**item))
        return users, count, total

    def get_app_requestable_permissions(
        self,
        app_id: UUID,
        search_term: str | None = None,
        all: bool = False
    ) -> Tuple[List[Permission], int, int]:
        endpoint = f"appstore/requestable_permissions"
        params: dict[str, Any] = {
            "app_id": str(app_id)
        }
        if (search_term):
            params["search_term"] = search_term
        
        raw_permissions, count, total, _, _ = self.get_all_or_paged(endpoint, params=params, all=all)
        
        return [self._create_permission(item) for item in raw_permissions], count, total
    
    def get_app_requestable_permission(self, permission_id: UUID) -> Permission | None:
        item = self.get(f"appstore/requestable_permissions/{permission_id}")
        if not item:
            return None
        return self._create_permission(item)
    
    def _create_permission(self, raw_permission: dict) -> Permission:
        permission = Permission(**raw_permission)
        durations = raw_permission["request_config"]["request_fulfillment_config"]["time_based_access"]
        permission.duration_options = durations
        return permission

    def create_access_request(
        self, 
        app_id: UUID,
        note: str,
        expiration_in_seconds: int | None,
        permission_ids: List[UUID] | None = None,
        target_user_id: UUID | None = None) -> AccessRequest | None:
        body: dict[str, Any] = {
            "app_id": str(app_id),
            "note": note,
        }
        if permission_ids:
            body["requestable_permission_ids"] = [str(p) for p in permission_ids]
        if expiration_in_seconds:
            body["expiration_in_seconds"] = expiration_in_seconds
        if target_user_id:
            body["target_user_id"] = str(target_user_id)
        response = self.post(
            "appstore/access_request",
            body
        )

        return AccessRequest(**response[0]) if response else None
