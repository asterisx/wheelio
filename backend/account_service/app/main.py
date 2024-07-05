from os import environ
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core_lib.consul import register_service
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from routers import account, user_info
from schemas import User, PrivacySetting

DATABASE_URL = environ["DATABASE_URL"]
DATABASE_NAME = environ["DATABASE_NAME"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    register_service()
    try:
        client = AsyncIOMotorClient(DATABASE_URL)
        await init_beanie(database=client[DATABASE_NAME], document_models=[User, PrivacySetting])
    except Exception as e:
        print(e)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(account.router)
app.include_router(user_info.router)
