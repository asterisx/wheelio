from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import Annotated


class Status(Document, BaseModel):
    username: Annotated[str, Field(..., min_length=1), Indexed(unique=True)]
    status: Annotated[str, Field(..., min_length=1)]


class StatusDTO(BaseModel):
    username: Annotated[str, Field(..., min_length=1)]
    status: Annotated[str, Field(..., min_length=1)]
