
from typing import Any, Dict, Tuple
import requests
from models import App, AccessRequest, Permission, SupportRequestStatus, User
from uuid import UUID
from typing import Any, Dict, List, Optional
from models import App, AccessRequest, Permission, User
from state import state

class BaseClient:
    def __init__(self):
        pass

    def get(self, endpoint: str, params: dict | None = None) -> Any:
        """Function to call an API endpoint and return the response."""
        url, headers = self._get_url_and_headers(endpoint)
        response = requests.get(url, headers=headers, params=params)
        if response.ok:
            return response.json()
        else:
            return None

    def post(self, endpoint: str, body: Dict[str, Any]) -> Any:
        """Function to call an API endpoint and return the response."""
        url, headers = self._get_url_and_headers(endpoint)
        response = requests.post(url, headers=headers, json=body)
        if response.ok:
            return response.json()
        else:
            return {"error": "Failed to post", "status_code": response.status_code}

    def _get_url_and_headers(self, endpoint: str) -> tuple[str, dict[str, str]]:
        api_key = state["api_key"]
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }
        return f"http://localhost:8000/{endpoint}", headers
    

client = BaseClient()
class Client:
    def __init__(self):
        pass

    def get_current_user(self) -> User:
        user = client.get("users/current")
        return User(**user)

    def get_appstore_app(self, id: UUID) -> App | None:
        raw_app = client.get(f"appstore/apps/{id}")
        if raw_app:
            return App(**raw_app)
        return None
    
    def get_appstore_apps(self, name_search: str | None = None) -> Tuple[List[App], int]:
        endpoint = "appstore/apps"
        if name_search:
            endpoint += f"?name_search={name_search}"
        raw_apps = client.get(endpoint)
        apps: List[App] = []
        for item in raw_apps["items"]:
            apps.append(App(**item))
        return apps, int(raw_apps["total"])
    
    def get_access_requests(
        self,
        app_id: UUID | None,
        target_user_id: UUID | None,
        status: List[str] | None) -> Tuple[List[AccessRequest], int]:
        params: dict[str, Any]= {}
        if app_id: 
            params["app_id"] = str(app_id)
        if target_user_id:
            params["target_user_id"] = str(target_user_id)
        if (status and len(status) > 0):
            params["statuses"] = [str(s) for s in status]

        raw_access_requests = client.get("appstore/access_requests", params=params)
        access_requests: List[AccessRequest] = []
        for item in raw_access_requests["items"]:
            access_requests.append(AccessRequest(**item))
        return access_requests, int(raw_access_requests["total"])
    
    def get_users(self, like: Optional[str] = None) -> Tuple[List[User], int]:
        endpoint = "users"

        if like:
            endpoint += f"?name_or_email_search={like}"
        raw_users = client.get(endpoint)

        users: List[User] = []
        for item in raw_users["items"]:
            users.append(User(**item))
        return users, int(raw_users["total"])

    def get_app_requestable_permissions(self, app_id: UUID, search_term: str | None = None) -> Tuple[List[Permission], int]:
        endpoint = f"appstore/requestable_permissions?app_id={app_id}"
        if (search_term):
            endpoint += f"&search_term={search_term}"
        
        raw_permissions = client.get(endpoint)
        
        permissions: List[Permission] = []
        for item in raw_permissions["items"]:
            permission = Permission(**item)
            durations = item["request_config"]["request_fulfillment_config"]["time_based_access"]
            permission.duration_options = durations
            permissions.append(permission)
        return permissions, int(raw_permissions["total"])
    
    def get_app_requestable_permission(self, permission_id: UUID) -> Permission:
        item = client.get(f"appstore/requestable_permissions/{permission_id}")
        permission = Permission(**item)
        durations = item["request_config"]["request_fulfillment_config"]["time_based_access"]
        permission.duration_options = durations
        return permission

    def create_access_request(
            self, 
            app_id: UUID,
            permission_ids: List[UUID],
            note: str,
            expiration_in_seconds: int | None,
            target_user_id: UUID | None) -> None:
        # TODO: expand to include expiration in seconds.
        # TODO: expand to include target user
        body: dict[str, Any] = {
            "app_id": str(app_id),
            "requestable_permission_ids": [str(p) for p in permission_ids],
            "note": note,
        }

        if expiration_in_seconds:
            body["expiration_in_seconds"] = expiration_in_seconds

        if target_user_id:
            body["target_user_id"] = str(target_user_id)
        client.post(
            "appstore/access_request",
            body
        )
