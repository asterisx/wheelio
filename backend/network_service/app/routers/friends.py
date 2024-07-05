from os import environ
from typing import List
from fastapi import APIRouter, Header, status
from core_lib.consul import get_consul_service_url
from core_lib.utils import fetch
from core_lib.values import OPENAPI_EXTRA_PROTECTED
from core_lib.schemas import StatusDTO
from models import Profile, UserStatus
from dependencies import get_friends_for_user
from schemas import ReportedContent
from motor.motor_asyncio import AsyncIOMotorClient

STATUS_SERVICE_URL = get_consul_service_url(environ["STATUS_SERVICE_NAME"])
DATABASE_URL = environ["DATABASE_URL"]
DATABASE_NAME = environ["DATABASE_NAME"]

router = APIRouter()

client = AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]


@router.get(
    "/friends",
    status_code=status.HTTP_200_OK,
    operation_id="getFriendsProfiles",
    response_model=List[Profile],
    responses={
        status.HTTP_200_OK: {
            "description": "List of friends and their profiles",
            "content": {
                "application/json": {
                    "example": {
                        "friends_profiles": [
                            {
                                "username": "user1",
                                "status": "Hi",
                                "report_content": "Report 1",
                            },
                            {
                                "username": "user2",
                                "status": "Hey!",
                                "report_content": "Report 2",
                            },
                        ]
                    }
                }
            },
        },
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def get_friends(
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
) -> List[Profile]:
    try:
        friends = await get_friends_for_user(current_user_name)
        statuses = await fetch(
            url=f"{STATUS_SERVICE_URL}/of-users",
            response_type=List[StatusDTO],
            json=friends,
        )
        friend_statuses = {status.username: status.status for status in statuses}
        reported_content = await ReportedContent.find(
            ReportedContent.reporter_username == current_user_name
        ).to_list()
        reported_users = {
            reported.reported_username: reported.content for reported in reported_content
        }
        result_profiles = []
        for friend in friends:
            friend_status = friend_statuses.get(friend, None)
            status = (
                UserStatus(
                    text=friend_status,
                    is_reported_by_user=friend in reported_users
                    and friend_status == reported_users.get(friend)
                )
                if friend_status is not None
                else None
            )
            result_profiles.append(
                Profile(
                    username=friend,
                    status=status
                    if friend_status is not None
                    else None,
                    is_friend_request_pending=False,
                    is_friend_request_requested=False,
                    is_friend=True
                )
            )

        return result_profiles
    except Exception as e:
        print(e)
