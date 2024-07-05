from os import environ
from core_lib.models import UserBase
from fastapi import APIRouter, HTTPException, status, Body, Header
from passlib.context import CryptContext
from core_lib.values import OPENAPI_EXTRA_PROTECTED
from schemas import User, UserCreds, PrivacySetting

SALT = environ["SALT"]

USERNAME_ALREADY_EXISTS = "Username already exists"
INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password"
INVALID_REQUEST = "Invalid Request"
SIGNUP_SUCCESSFUL = "Signup successful"
LOGIN_SUCCESSFUL = "Login successful"
LOGOUT_SUCCESSFUL = "Logged out successfully"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_200_OK,
    operation_id="signupUser",
    responses={
        status.HTTP_200_OK: {
            "description": SIGNUP_SUCCESSFUL,
            "content": {
                "application/json": {"example": {"message": SIGNUP_SUCCESSFUL}}
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": USERNAME_ALREADY_EXISTS,
            "content": {
                "application/json": {"example": {"message": USERNAME_ALREADY_EXISTS}}
            },
        },
    },
)
async def signup(user: UserCreds = Body(...)):
    existing_user = await User.find_one(User.username == user.username.strip().lower())
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=USERNAME_ALREADY_EXISTS
        )
    hashed_password = pwd_context.hash(user.password + SALT)
    new_user = User(username=user.username.strip().lower(), password=hashed_password)
    await new_user.insert()

    privacy_setting = PrivacySetting(username=new_user.username, profile_private=False)
    await privacy_setting.insert()

    return {"message": SIGNUP_SUCCESSFUL}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    operation_id="loginUser",
    responses={
        status.HTTP_200_OK: {
            "description": LOGIN_SUCCESSFUL,
            "content": {"application/json": {"example": {"message": LOGIN_SUCCESSFUL}}},
        },
        status.HTTP_400_BAD_REQUEST: {"description": INCORRECT_USERNAME_OR_PASSWORD},
    },
)
async def login(user: UserCreds = Body(...)):
    db_user_data = await User.find_one(User.username == user.username.strip().lower())
    if not db_user_data or not pwd_context.verify(
        user.password + SALT, db_user_data.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=INCORRECT_USERNAME_OR_PASSWORD,
        )
    return {"message": LOGIN_SUCCESSFUL}


@router.get(
    "/me",
    response_model=UserBase,
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def get_current_user(
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    if not current_user_name:
        return
    return {"username": current_user_name}


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    operation_id="logoutUser",
    responses={
        status.HTTP_200_OK: {"description": LOGOUT_SUCCESSFUL},
        status.HTTP_400_BAD_REQUEST: {"description": INVALID_REQUEST},
    },
)
async def logout():
    return {"message": LOGOUT_SUCCESSFUL}
