from os import environ
from fastapi import FastAPI, HTTPException, Header, status, Body
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from beanie.operators import In
from core_lib.consul import register_service
from core_lib.values import OPENAPI_EXTRA_PROTECTED
from core_lib.schemas import Status
from rabbit import Rabbit
from beanie import init_beanie

DATABASE_URL = environ["DATABASE_URL"]
DATABASE_NAME = environ["DATABASE_NAME"]

STATUS_CREATED_SUCCESSFULLY = "Status created successfully"
STATUS_UPDATED_SUCCESSFULLY = "Status updated successfully"

rabbit = Rabbit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    register_service()
    client = AsyncIOMotorClient(DATABASE_URL)
    await init_beanie(
        database=client[DATABASE_NAME], document_models=[Status]
    )

    await rabbit.connect()
    yield
    await client.close()
    await rabbit.diconnect()


app = FastAPI(lifespan=lifespan)


@app.get(
    "/get",
    status_code=status.HTTP_200_OK,
    operation_id="getStatus",
    response_model=Status,
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def get_status(
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    status = await Status.find_one(Status.username == current_user_name)
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Status not found"
        )
    return status


@app.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    operation_id="createStatus",
    responses={
        201: {
            "description": STATUS_CREATED_SUCCESSFULLY,
            "content": {
                "application/json": {
                    "example": {"message": STATUS_CREATED_SUCCESSFULLY}
                }
            },
        },
    },
    openapi_extra=OPENAPI_EXTRA_PROTECTED,
)
async def create_status(
    status: str = Body(..., min_length=1),
    current_user_name: str = Header(
        None, alias="X-Current-User-Name", include_in_schema=False
    ),
):
    existing_status = await Status.find_one(Status.username == current_user_name)
    if existing_status:
        existing_status.status = status
        try:
            await existing_status.save()
        except Exception as e:
            print(e)
        await rabbit.publish_status_create_event(status=existing_status)
    else:
        new_status = Status(username=current_user_name, status=status)
        await new_status.insert()
        await rabbit.publish_status_create_event(status=new_status)
    return {"message": STATUS_CREATED_SUCCESSFULLY}


@app.post(
    "/of-users",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
    openapi_extra={"x-internal": True},
)
async def get_statuses(
    usernames: List[str] = Body(...),
) -> List[Status]:
    statuses = await Status.find(In(Status.username, usernames)).to_list()
    print(usernames, [
        Status(username=status.username, status=status.status) for status in statuses
    ])
    return [
        Status(username=status.username, status=status.status) for status in statuses
    ]
