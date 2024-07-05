from jwt import encode, decode, PyJWTError
from os import environ
from datetime import datetime, timedelta
from fastapi import Request
from typing import Optional

SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(environ["ACCESS_TOKEN_EXPIRE_MINUTES"])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_username(request: Request) -> str:
    token = request.cookies.get("session_token")
    if not token:
        return None
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except PyJWTError:
        return None


async def validate_session(request: Request) -> bool:
    token = request.cookies.get("session_token")
    if not token:
        return False
    try:
        decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except PyJWTError:
        return False


def create_session(username: str) -> str:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return access_token
