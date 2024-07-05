from typing import Annotated
from beanie import Document, Indexed
from core_lib.models import UserBase
from pydantic import Field


class UserCreds(UserBase):
    password: Annotated[str, Field(..., min_length=1)]


class User(Document, UserCreds):
    pass


class PrivacySetting(Document):
    username: Annotated[str, Field(...), Indexed(unique=True)]
    profile_private: Annotated[bool, Field(...)]
