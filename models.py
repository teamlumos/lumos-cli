from uuid import UUID
from pydantic import BaseModel
from typing import Optional
import pytz

class App(BaseModel):
    id: UUID
    user_friendly_label: str
    app_class_id: str
    instance_id: str

    def __str__(self):
        return self.user_friendly_label
    
    def tabulate(self):
        return [self.id, self.user_friendly_label]
    
    @staticmethod   
    def headers():
        return ["ID", "App"]

class Permission(BaseModel):
    id: UUID
    label: str
    app_id: str
    app_class_id: str
    duration_options: list[str] = []

    def __str__(self):
        return self.label

    def tabulate(self):
        return [self.id, self.label, ', '.join(self.duration_options)]
    
    @staticmethod
    def headers():
        return ["ID", "Permission", "Access length options"]

class User(BaseModel):
    id: UUID
    given_name: str
    family_name: str
    email: str

    def __str__(self):
        return f"{self.given_name} {self.family_name} ({self.email})"
    
    def tabulate(self):
        return [f"{self.given_name} {self.family_name}", self.email, self.id]
    
    @staticmethod
    def headers():
        return ["Name", "Email", "ID"]

class AccessRequest(BaseModel):
    id: UUID
    app_name: str
    status: str
    requested_at: str
    expires_at: Optional[str]
    requester_user: User
    supporter_user: Optional[User]
    target_user: User
    requestable_permission_ids: list[UUID]
    permissions: list[Permission] = []

    @staticmethod
    def _convert_to_human_date(inp: str) -> str:
        if not inp:
            return ""
        import datetime

        # Parse the input UTC time string to a datetime object
        utc_time = datetime.datetime.strptime(inp, "%Y-%m-%dT%H:%M:%S")
        
        # Set the timezone to UTC for the parsed datetime
        utc_time = utc_time.replace(tzinfo=pytz.utc)
        
        # Convert UTC time to EST
        est_time = utc_time.astimezone(pytz.timezone('America/New_York'))
        
        # Format the EST time into a more human-readable string
        human_date = est_time.strftime("%a %b %d, %Y %I:%M %p EST")
        
        return human_date

    def __str__(self):
        return f"{self.app_name} ({self.status})"
    
    def tabulate(self):
        return [
            self.id,
            self.app_name,
            '\n'.join([p.label for p in self.permissions]) or '-----',
            self.requester_user.given_name + " " + self.requester_user.family_name,
            self.target_user.given_name + " " + self.target_user.family_name if self.requester_user.id != self.target_user.id else "(self)",
            self.status,
            self._convert_to_human_date(self.requested_at),
            self._convert_to_human_date(self.expires_at)]
    
    @staticmethod
    def headers():
        return ["ID", "App", "Permissions", "Requester", "For", "Status", "Requested at", "Expires at"]


# If this enum is updated both this table as well as SupportRequestComments must be updated.
class SupportRequestStatus:
    # initial status, right after creating a request, no action should be taken on the request
    # at this stage
    PENDING = "PENDING"
    # after recognizing the manager approval for the request is required, it's waiting for manager
    PENDING_MANAGER_APPROVAL = "PENDING_MANAGER_APPROVAL"
    # after a manager approves it
    MANAGER_APPROVED = "MANAGER_APPROVED"
    # when a manager rejects it
    MANAGER_DENIED = "MANAGER_DENIED"
    # after recognizing the approval for the request is required, it's waiting for end-user
    PENDING_APPROVAL = "PENDING_APPROVAL"
    # after an approver approves it or assigned automatically when there is no need for approval
    APPROVED = "APPROVED"
    # when an approver rejects it
    DENIED = "DENIED"
    # assigned automatically when neither the approver or admin completes the request in time
    EXPIRED = "EXPIRED"
    # after user cancels the request
    CANCELLED = "CANCELLED"
    # when the request enters provisioning and it's still not clear whether it'll happen
    # automatically or we will need to ask for manual provisioning
    PENDING_PROVISIONING = "PENDING_PROVISIONING"
    # after recognizing the provisioning for the request needs to be done manually,
    # it's waiting for end-user
    PENDING_MANUAL_PROVISIONING = "PENDING_MANUAL_PROVISIONING"
    # when admin denied the request
    DENIED_PROVISIONING = "DENIED_PROVISIONING"
    # after either the manual or automatic provisioning,
    # when it's waiting for the final "cleanup" on our end
    PROVISIONED = "PROVISIONED"
    # when a time based request has been completed and the time has elapsed but automatic removal
    # failed and access needs to be manually removed
    PENDING_MANUAL_DEPROVISIONING = "PENDING_MANUAL_DEPROVISIONING"
    # when the request has been completed and access has been removed because the request was
    # only for a limited amount of time
    TIME_BASED_EXPIRED = "TIME_BASED_EXPIRED"
    # when the request has been fully finalized and there are no more actions pending
    COMPLETED = "COMPLETED"
    # when the request has been marked to be reverted by a user via the "Undo an action" flow
    # but before the actual reverting is completed
    REVERTING = "REVERTING"
    # when the request has been fully reverted
    REVERTED = "REVERTED"

    PENDING_STATUSES = [
        PENDING,
        PENDING_MANAGER_APPROVAL,
        PENDING_APPROVAL,
        PENDING_PROVISIONING
    ]