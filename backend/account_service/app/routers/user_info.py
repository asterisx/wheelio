from typing import List
from core_lib.models import UserBase, UserWithPrivacy
from fastapi import APIRouter, Query, status, HTTPException, Header
from schemas import User, PrivacySetting

USER_NOT_FOUND = "User not found"

router = APIRouter()


@router.post(
    "/user-info/{username}",
    status_code=status.HTTP_200_OK,
    response_model=UserBase,
    include_in_schema=False,
    openapi_extra={"x-internal": True},
)
async def get_user_from_user_name(username: str) -> User:
    user = await User.find_one(User.username == username)
    if user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return UserBase(username=user.username)


@router.get(
    "/privacy-setting",
    status_code=status.HTTP_200_OK,
    operation_id="getPrivacy",
    response_model=PrivacySetting,
)
async def get_privacy_setting(
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    return await PrivacySetting.find_one(PrivacySetting.username == current_user_name)


@router.post(
    "/set-privacy",
    status_code=status.HTTP_200_OK,
    operation_id="setPrivacy",
)
async def set_privacy(
    profile_private: bool,
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    privacy_setting = await PrivacySetting.find_one(
        PrivacySetting.username == current_user_name
    )
    if privacy_setting:
        privacy_setting.profile_private = profile_private
        await privacy_setting.save()
    else:
        privacy_setting = PrivacySetting(
            username=current_user_name, profile_private=profile_private
        )
        await privacy_setting.insert()
    return {"profile_private": privacy_setting.profile_private}


@router.post(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=List[UserWithPrivacy],
    include_in_schema=False,
    openapi_extra={"x-internal": True},
)
async def get_all_users(search: str = Query(None)) -> List[UserWithPrivacy]:
    query = {}
    if search:
        query = {"username": {"$regex": search, "$options": "i"}}
    users = await User.find_many(query).to_list()
    usernames = [user.username for user in users]
    privacy_settings = await PrivacySetting.find_many(
        {"username": {"$in": usernames}}
    ).to_list()
    usernames = [user.username for user in users]

    privacy_settings = await PrivacySetting.find_many(
        {"username": {"$in": usernames}}
    ).to_list()
    privacy_dict = {privacy.username: privacy for privacy in privacy_settings}

    return [
        UserWithPrivacy(
            username=user.username,
            profile_private=privacy_dict.get(user.username).profile_private
            if privacy_dict.get(user.username)
            else None,
        )
        for user in users
    ]

