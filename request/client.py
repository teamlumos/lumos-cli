# client.py

from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import requests

API_TOKEN = "lsk_kKSWQAh1YAwWKgmj2Ppbg1jLVB5PVKY7VoBRJK-spCeA"


class App(BaseModel):
    id: str
    user_friendly_label: str
    app_class_id: str
    instance_id: str

    def __str__(self):
        return self.user_friendly_label

class Permission(BaseModel):
    id: str
    label: str
    app_id: str
    app_class_id: str

    def __str__(self):
        return self.label

class User(BaseModel):
    email: str

class AccessRequest(BaseModel):
    id: str
    app_name: str
    status: str
    requested_at: str
    requester_user: User
    supporter_user: Optional[User]
    target_user: User

class Client:
    def __init__(self):
        pass

    def get_appstore_apps(self) -> List[App]:
        raw_apps = self._get("appstore/apps")

        apps: List[App] = []
        for item in raw_apps["items"]:
            apps.append(App(**item))
        return apps
    
    def get_access_requests(self) -> List[AccessRequest]:
        raw_access_requests = self._get("appstore/access_requests?&page=1&size=100")

        access_requests: List[AccessRequest] = []
        for item in raw_access_requests["items"]:
            access_requests.append(AccessRequest(**item))
        return access_requests

    def get_app_requestable_permissions(self, app_id: str) -> List[Permission]:
        raw_permissions = self._get(f"appstore/requestable_permissions?app_id={app_id}")

        permissions: List[Permission] = []
        for item in raw_permissions["items"]:
            permissions.append(Permission(**item))
        return permissions

    def create_access_request(self, app_id: str, permission_ids: List[str], note: str) -> None:
        # TODO: expand to include expiration in seconds.
        # TODO: expand to include target user
        self._post(
            "appstore/access_request",
            body={
                "app_id": app_id,
                "requestable_permission_ids": permission_ids,
                "note": note,
            }
        )

    def _get(self, endpoint: str) -> Any:
        """Function to call an API endpoint and return the response."""
        url = f"http://localhost:8000/{endpoint}"
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        else:
            return {"error": "Failed to fetch data", "status_code": response.status_code}
        
    def _post(self, endpoint: str, body: Dict[str, Any]) -> Any:
        """Function to call an API endpoint and return the response."""
        url = f"http://localhost:8000/{endpoint}"
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json",
        }
        response = requests.post(url, headers=headers, json=body)
        if response.ok:
            return response.json()
        else:
            return {"error": "Failed to post", "status_code": response.status_code}