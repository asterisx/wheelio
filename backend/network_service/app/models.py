from typing import Optional
from pydantic import Field, BaseModel
from core_lib.models import UserBase


class UserStatus(BaseModel):
    text: str = Field(None, description="Status text of the user")
    is_reported_by_current_user: bool = Field(
        False, description="Indicates if the status is reported by current user"
    )


class Profile(UserBase):
    is_friend: bool = Field(..., description="Indicates if the user is a friend")
    is_friend_request_pending: bool = Field(
        ..., description="Indicates if a friend request is pending"
    )
    is_friend_request_requested: bool = Field(
        ..., description="Indicates if a friend request has been requested"
    )
    status: Optional[UserStatus]

class ReportContentRequest(BaseModel):
    status: str
