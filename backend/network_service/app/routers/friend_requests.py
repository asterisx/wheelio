from os import environ
from fastapi import APIRouter, HTTPException, Header, status
from typing import List
from core_lib.consul import get_consul_service_url
from core_lib.utils import fetch
from core_lib.models import (
    FriendRequestNotification,
    FriendRequestAcceptedNotification,
    UserBase,
)
from core_lib.values import OPENAPI_EXTRA_PROTECTED
from schemas import FriendRequest, Friend, BlockedUser
from motor.motor_asyncio import AsyncIOMotorClient
from rabbit import Rabbit

rabbit = Rabbit()

ACCOUNT_SERVICE_NAME = environ["ACCOUNT_SERVICE_NAME"]
DATABASE_URL = environ["DATABASE_URL"]

FRIEND_REQUEST_SENT = "Friend request sent"
INVALID_REQUEST = "Invalid request"
USER_NOT_FOUND = "User not found"
FRIEND_REQUEST_ACCEPTED = "Friend request accepted"
FRIEND_REQUEST_NOT_FOUND = "Friend request not found"
FRIEND_REQUEST_ALREADY_EXISTS = "Friend request already exists"
USER_BLOCKED = "User is blocked"

router = APIRouter()


@router.post(
    "/send_friend_request/{username}",
    operation_id="sendFriendRequest",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": FRIEND_REQUEST_SENT,
            "content": {
                "application/json": {"example": {"message": FRIEND_REQUEST_SENT}}
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": INVALID_REQUEST},
        status.HTTP_404_NOT_FOUND: {"description": USER_NOT_FOUND},
        status.HTTP_409_CONFLICT: {"description": FRIEND_REQUEST_ALREADY_EXISTS},
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def send_friend_request(
    username: str,
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    try:
        user = await fetch(
            url=f"{get_consul_service_url(ACCOUNT_SERVICE_NAME)}/user-info/{username}",
            response_type=UserBase,
        )
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
            )
        else:
            raise e

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND
        )

    existing_request = await FriendRequest.find_one(
        FriendRequest.sender_username == current_user_name,
        FriendRequest.receiver_username == username,
    )
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FRIEND_REQUEST_ALREADY_EXISTS,
        )

    blocked_user = await BlockedUser.find_one(
        BlockedUser.blocker_username == current_user_name,
        BlockedUser.blocked_username == username,
    )
    if blocked_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USER_BLOCKED,
        )

    new_request = FriendRequest(
        sender_username=current_user_name, receiver_username=username
    )
    await new_request.insert()

    await rabbit.send_notification(
        notification=FriendRequestNotification(
            receiver_username=username,
            sender_username=current_user_name,
        )
    )

    return {"message": FRIEND_REQUEST_SENT}


@router.post(
    "/accept_friend_request/{username}",
    operation_id="acceptFriendRequest",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": FRIEND_REQUEST_ACCEPTED,
            "content": {
                "application/json": {"example": {"message": FRIEND_REQUEST_ACCEPTED}}
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": INVALID_REQUEST},
        status.HTTP_404_NOT_FOUND: {"description": FRIEND_REQUEST_NOT_FOUND},
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def accept_friend_request(
    username: str,
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    existing_friend_request: FriendRequest = await FriendRequest.find_one(
        FriendRequest.sender_username == username,
        FriendRequest.receiver_username == current_user_name,
    )
    if not existing_friend_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=FRIEND_REQUEST_NOT_FOUND
        )

    blocked_user = await BlockedUser.find_one(
        BlockedUser.blocker_username == current_user_name,
        BlockedUser.blocked_username == username,
    )
    if blocked_user:
        await FriendRequest.find_one(
            FriendRequest.sender_username == username,
            FriendRequest.receiver_username == current_user_name,
        ).delete()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=USER_BLOCKED,
        )

    client = AsyncIOMotorClient(DATABASE_URL)
    async with await client.start_session() as session:
        async with session.start_transaction():
            try:
                friend = Friend(username=current_user_name, friend_username=username)
                await friend.insert()
                friend = Friend(username=username, friend_username=current_user_name)
                await friend.insert()
                await FriendRequest.find_one(
                    FriendRequest.sender_username == username,
                    FriendRequest.receiver_username == current_user_name,
                ).delete()
            except Exception:
                await session.abort_transaction()

    await rabbit.send_notification(
        notification=FriendRequestAcceptedNotification(
            receiver_username=username,
            friend_username=current_user_name,
        )
    )
    return {"message": FRIEND_REQUEST_ACCEPTED}


@router.get(
    "/requests",
    operation_id="getFriendRequests",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "List of usernames of users who have sent friend requests to the current user",
            "content": {
                "application/json": {"example": {"requests": ["user1", "user2"]}}
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": INVALID_REQUEST},
        status.HTTP_404_NOT_FOUND: {"description": FRIEND_REQUEST_NOT_FOUND},
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def get_requests(
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
) -> List[str]:
    pending_requests: List[FriendRequest] = await FriendRequest.find(
        FriendRequest.receiver_username == current_user_name
    ).to_list()
    return [request.sender_username for request in pending_requests]


