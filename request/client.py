# client.py

from typing import Any, Dict, List, Optional
import requests

API_TOKEN = "lsk_kKSWQAh1YAwWKgmj2Ppbg1jLVB5PVKY7VoBRJK-spCeA"

from pydantic import BaseModel

class App(BaseModel):
    id: str
    user_friendly_label: str
    app_class_id: str
    instance_id: str

class Permission(BaseModel):
    id: str
    label: str
    app_id: str
    app_class_id: str

class Client:
    def __init__(self):
        pass

    def get_appstore_apps(self) -> List[App]:
        raw_apps = self._get("appstore/apps")

        apps: List[App] = []
        for item in raw_apps["items"]:
            apps.append(App(**item))
        return apps

    def get_app_requestable_permissions(self, app_id: str) -> List[Permission]:
        raw_permissions = self._get(f"appstore/requestable_permissions?app_id={app_id}")

        permissions: List[Permission] = []
        for item in raw_permissions["items"]:
            permissions.append(Permission(**item))
        return permissions

    def create_access_request(self, app_id: str, permission_id: str, target_user_id: str, note: str) -> None:
        # TODO(alanefl) expand to a list of permission_id.
        # TODO(alanefl) expand to include expiration in seconds.
        self._post(
            "appstore/access_request",
            body={
                "app_id": app_id,
                "requestable_permission_ids": [permission_id],
                "target_user_id": target_user_id,
                "note": note,
                # "expiration_in_seconds": str(expiration_in_seconds)
            }
        )
        return "launched!"

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