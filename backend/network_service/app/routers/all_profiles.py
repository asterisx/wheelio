from os import environ
from fastapi import APIRouter, status, Query, Header
from typing import List, Optional
from core_lib.consul import get_consul_service_url
from core_lib.utils import fetch
from core_lib.models import UserWithPrivacy
from core_lib.schemas import StatusDTO
from schemas import Friend, FriendRequest, BlockedUser, ReportedContent
from models import Profile, UserStatus


STATUS_SERVICE_URL = get_consul_service_url(environ["STATUS_SERVICE_NAME"])
ACCOUNT_SERVICE_URL = get_consul_service_url(environ["ACCOUNT_SERVICE_NAME"])

router = APIRouter()


@router.get(
    "/all-profiles",
    operation_id="getAllUsers",
    status_code=status.HTTP_200_OK,
    response_model=List[Profile],
    responses={
        status.HTTP_200_OK: {
            "description": "List of all users and their relationship status",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "username": "user1",
                            "is_friend": True,
                            "is_pending": False,
                            "is_requested": False,
                            "status": {
                                "text": "Hi",
                                "is_reported_by_current_user": False,
                            },
                        },
                        {
                            "username": "user2",
                            "is_friend": False,
                            "is_pending": True,
                            "is_requested": False,
                            "status": {
                                "text": "Hey!",
                                "is_reported_by_current_user": True,
                            },
                        },
                    ]
                }
            },
        },
    },
)
async def get_all_profiles(
    search: Optional[str] = Query(
        None, description="Search parameter for filtering users by username"
    ),
    current_user_name: Optional[str] = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
) -> List[Profile]:
    params = {"search": search} if search else {}
    all_users_with_privacy = await fetch(
        url=f"{ACCOUNT_SERVICE_URL}/users",
        response_type=List[UserWithPrivacy],
        params=params,
    )

    friends_usernames: set[str] = set()
    requesters: set[str] = set()
    requested: set[str] = set()
    blocked_usernames: set[str] = set()
    blocked_by_usernames: set[str] = set()
    reported_content: dict[str, str] = {}

    if current_user_name:
        friends = await Friend.find(Friend.username == current_user_name).to_list()
        friends_usernames = {friend.friend_username for friend in friends}
        pending_requests = await FriendRequest.find(
            FriendRequest.sender_username == current_user_name
        ).to_list()
        requesters = {request.receiver_username for request in pending_requests}

        requested_friends = await FriendRequest.find(
            FriendRequest.receiver_username == current_user_name
        ).to_list()
        requested = {request.sender_username for request in requested_friends}

        blocked_users = await BlockedUser.find(
            BlockedUser.blocker_username == current_user_name
        ).to_list()
        blocked_usernames = {blocked.blocked_username for blocked in blocked_users}

        blocked_by_users = await BlockedUser.find(
            BlockedUser.blocked_username == current_user_name
        ).to_list()
        blocked_by_usernames = {
            blocked.blocker_username for blocked in blocked_by_users
        }

        reported_users = await ReportedContent.find(
            ReportedContent.reporter_username == current_user_name
        ).to_list()
        reported_content = {
            reported.reported_username: reported.content for reported in reported_users
        }

    other_users = [
        user.username
        for user in all_users_with_privacy
        if user.username != current_user_name
    ]
    statuses = await fetch(
        url=f"{STATUS_SERVICE_URL}/of-users",
        response_type=List[StatusDTO],
        json=other_users,
    )

    status_dict = {status.username: status.status for status in statuses}
    profiles = []
    for user in all_users_with_privacy:
        user_status = status_dict.get(user.username)
        if user.username == current_user_name:
            continue
        if current_user_name:
            if (
                user.username in blocked_usernames
                or user.username in blocked_by_usernames
            ):
                continue
            if user.profile_private and user.username not in friends_usernames:
                continue

            status = (
                UserStatus(
                    text=user_status,
                    is_reported_by_current_user=user.username in reported_content
                    and user_status == reported_content.get(user.username),
                )
                if user_status is not None
                else None
            )
            profiles.append(
                Profile(
                    username=user.username,
                    is_friend=user.username in friends_usernames,
                    is_friend_request_pending=user.username in requesters,
                    is_friend_request_requested=user.username in requested,
                    status=status,
                )
            )
        else:
            status = (
                UserStatus(
                    text=user_status,
                    is_reported_by_current_user=False
                )
                if user_status is not None
                else None
            )
            profiles.append(
                Profile(
                    username=user.username,
                    status=status,
                    is_friend_request_pending=False,
                    is_friend_request_requested=False,
                    is_friend=False,
                )
            )
    return profiles
