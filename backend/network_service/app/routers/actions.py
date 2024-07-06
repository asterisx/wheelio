from os import environ
from typing import List
from fastapi import APIRouter, Header, HTTPException, status
from core_lib.values import OPENAPI_EXTRA_PROTECTED
from core_lib.consul import get_consul_service_url
from core_lib.utils import fetch
from core_lib.models import UserBase
from core_lib.schemas import StatusDTO
from schemas import BlockedUser, ReportedContent, Friend

STATUS_SERVICE_URL = get_consul_service_url(environ["STATUS_SERVICE_NAME"])
ACCOUNT_SERVICE_URL = get_consul_service_url(environ["ACCOUNT_SERVICE_NAME"])

router = APIRouter()

@router.post(
    "/block_user/{username}",
    operation_id="blockUser",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "User blocked successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def block_user(
    username: str,
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    user = await fetch(
        url=f"{ACCOUNT_SERVICE_URL}/user-info/{username}",
        response_type=UserBase,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    friend = await Friend.find_one(
        Friend.username == current_user_name, Friend.friend_username == username
    )
    if friend:
        await friend.delete()
        reverse_friend = await Friend.find_one(
            Friend.username == username, Friend.friend_username == current_user_name
        )
        if reverse_friend:
            await reverse_friend.delete()

    blocked_user = BlockedUser(
        blocker_username=current_user_name, blocked_username=username
    )
    await blocked_user.insert()

    return {"message": "User blocked successfully"}


@router.post(
    "/report_content/{username}",
    operation_id="reportContent",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"description": "Content reported successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def report_content(
    username: str,
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    user = await fetch(
        url=f"{ACCOUNT_SERVICE_URL}/user-info/{username}",
        response_type=UserBase,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    status_response = await fetch(
        url=f"{STATUS_SERVICE_URL}/of-users",
        response_type=List[StatusDTO],
        json=[username],
    )
    user_status = status_response[0].status if status_response else None

    reported_content = ReportedContent(
        reporter_username=current_user_name,
        reported_username=username,
        content=user_status,
    )
    await reported_content.insert()

    return {"message": "Content reported successfully"}
