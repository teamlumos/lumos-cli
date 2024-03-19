
from typing import Any, Dict, Tuple
import requests
from common.models import App, AccessRequest, Permission, SupportRequestStatus, User
from uuid import UUID
from typing import Any, Dict, List, Optional
from common.models import App, AccessRequest, Permission, User
import os
import typer

class BaseClient:
    API_URL="https://api.lumos.com"
    def __init__(self):
        pass
    
    def get(self, endpoint: str, params: dict | None = None):
        """Function to call an API endpoint and return the response."""
        return self._send_request("GET", endpoint, params=params)
    
    def get_paged(
        self,
        endpoint: str, 
        params: dict | None = None
    ) -> Tuple[List[dict[str, Any]], int, int, int, int]:
        """Function to call an API endpoint and return the paged response."""
        response = self.get(endpoint, params=params)
        if response:
            return response["items"], len(response["items"]), int(response["total"]), int(response["page"]), int(response["pages"])
        return [], 0, 0, 0, 0

    def post(self, endpoint: str, body: Dict[str, Any]):
        """Function to call an API endpoint and return the response."""
        return self._send_request("POST", endpoint, body=body)
    
    def _send_request(self,
        method: str,
        endpoint: str,
        body: dict | None = None,
        params: dict | None = None
    ):
        url, headers = self._get_url_and_headers(endpoint)
        response = requests.request(method, url, headers=headers, json=body, params=params)
        if response.ok:
            return response.json()
        if response.status_code == 403 or response.status_code == 401:
            typer.echo("Something went wrong. Check your API token.", err=True)
        else:
            typer.echo(f"An error occurred (status code {response.status_code})", err=True)
            typer.echo(f"    {response.json()['detail']}", err=True)
        raise typer.Exit(1)

    def _get_url_and_headers(self, endpoint: str) -> tuple[str, dict[str, str]]:
        api_key = os.environ.get("API_KEY")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "User-Agent": "lumos-cli/0.1.0",
        }
        return f"{self._get_api_url()}/{endpoint}", headers
    
    def _get_api_url(self) -> str:
        api_url: str | None = None
        if (os.environ.get("DEV_MODE")):
            api_url = os.environ.get("API_URL")
        return api_url or self.API_URL
    
class Client(BaseClient):
    def __init__(self):
        pass

    def get_current_user_id(self) -> str | None:
        if not os.environ.get("USER_ID"):
            user = self.get_current_user()
            if user:
                os.environ["USER_ID"] = str(user.id)
        return os.environ["USER_ID"]
    
    def get_current_user(self) -> User | None:
        user = self.get("users/current")
        if user:
            os.environ["USER_ID"] = user["id"]
            return User(**user)
        return None

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
    
    def get_appstore_apps(self, name_search: str | None = None) -> Tuple[List[App], int, int]:
        endpoint = "appstore/apps"
        params: dict[str, Any] = {}
        if name_search:
            params["name_search"] = name_search
        raw_apps, count, total, _, _ = self.get_paged(endpoint, params=params)
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
        count: int = 25
    ) -> Tuple[List[AccessRequest], int, int, int, int]:
        params: dict[str, Any]= {
            "page": page,
            "count": count
        }
        if target_user_id:
            params["target_user_id"] = str(target_user_id)
        if (status and len(status) > 0):
            params["statuses"] = [str(s) for s in status]

        raw_access_requests, count, total, page, pages = self.get_paged("appstore/access_requests", params=params)
        access_requests: List[AccessRequest] = []
        for item in raw_access_requests:
            access_request = self._create_access_request(item)
            if (access_request): 
                access_requests.append(access_request)
        return sorted(access_requests, key=lambda x: x.requested_at, reverse=True), count, total, page, pages
    
    def get_users(self, like: Optional[str] = None) -> Tuple[List[User], int, int]:
        endpoint = "users"
        params: dict[str, Any] = {}
        if like:
            params["search_term"] = like
        raw_users, count, total, _, _ = self.get_paged(endpoint, params=params)

        users: List[User] = []
        for item in raw_users:
            users.append(User(**item))
        return users, count, total

    def get_app_requestable_permissions(
        self,
        app_id: UUID,
        search_term: str | None = None
    ) -> Tuple[List[Permission], int, int]:
        endpoint = f"appstore/requestable_permissions"
        params: dict[str, Any] = {
            "app_id": str(app_id)
        }
        if (search_term):
            params["search_term"] = search_term
        
        raw_permissions, count, total, _, _ = self.get_paged(endpoint, params=params)
        
        return [self._create_permission(item) for item in raw_permissions], count, total
    
    def get_app_requestable_permission(self, permission_id: UUID) -> Permission:
        item = self.get(f"appstore/requestable_permissions/{permission_id}")
        return self._create_permission(item)
    
    def _create_permission(self, raw_permission: dict | None) -> Permission:
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
