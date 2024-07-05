from typing import Annotated, Union
from pydantic import BaseModel, Field
from beanie import Indexed
from enum import Enum


class EventType(str, Enum):
    FRIEND_REQUEST = "friend_request"
    FRIEND_REQUEST_ACCEPTED = "friend_request_accepted"
    STATUS = "status"


class NotificationBase(BaseModel):
    receiver_username: str
    event: EventType


class FriendRequestNotification(NotificationBase):
    event: EventType = EventType.FRIEND_REQUEST
    sender_username: str


class FriendRequestAcceptedNotification(NotificationBase):
    event: EventType = EventType.FRIEND_REQUEST_ACCEPTED
    friend_username: str


class StatusNotification(NotificationBase):
    event: EventType = EventType.STATUS
    status: str
    username: str


Notification = Union[
    FriendRequestNotification, FriendRequestAcceptedNotification, StatusNotification
]


class NotificationWrapper(NotificationBase):
    @classmethod
    def parse(cls, obj) -> Notification:
        event_type = obj.get("event")
        if event_type == EventType.FRIEND_REQUEST:
            return FriendRequestNotification.model_validate(obj)
        elif event_type == EventType.FRIEND_REQUEST_ACCEPTED:
            return FriendRequestAcceptedNotification.model_validate(obj)
        elif event_type == EventType.STATUS:
            return StatusNotification.model_validate(obj)


class UserBase(BaseModel):
    username: Annotated[str, Field(..., min_length=1), Indexed(unique=True)]


class UserWithPrivacy(UserBase):
    profile_private: bool
