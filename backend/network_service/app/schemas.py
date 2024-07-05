from beanie import Document
from pydantic import Field
from typing import Annotated


class FriendRequest(Document):
    sender_username: Annotated[str, Field(...)]
    receiver_username: Annotated[str, Field(...)]


class Friend(Document):
    username: Annotated[str, Field(...)]
    friend_username: Annotated[str, Field(...)]

    class Settings:
        collection = "friend"
        indexes = [
            "username",
        ]


class BlockedUser(Document):
    blocker_username: Annotated[str, Field(...)]
    blocked_username: Annotated[str, Field(...)]


class ReportedContent(Document):
    reporter_username: Annotated[str, Field(...)]
    reported_username: Annotated[str, Field(...)]
    content: Annotated[str, Field(...)]
