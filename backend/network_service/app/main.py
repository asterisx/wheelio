from os import environ
from fastapi import FastAPI
from contextlib import asynccontextmanager
from core_lib.consul import register_service
from routers import all_profiles, friends, friend_requests, actions
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from rabbit import Rabbit
from schemas import FriendRequest, Friend, BlockedUser, ReportedContent

DATABASE_URL = environ["DATABASE_URL"]
DATABASE_NAME = environ["DATABASE_NAME"]

@asynccontextmanager
async def lifespan(_: FastAPI):
    register_service()
    client = AsyncIOMotorClient(DATABASE_URL)
    await init_beanie(
        database=client[DATABASE_NAME],
        document_models=[FriendRequest, Friend, BlockedUser, ReportedContent],
    )

    rabbit = Rabbit()
    await rabbit.connect()
    import asyncio
    import threading

    loop = asyncio.get_event_loop()
    threading.Thread(
        target=lambda: asyncio.run_coroutine_threadsafe(rabbit.start_consuming(), loop)
    ).start()

    yield
    await client.close()
    await rabbit.close_connection()


app = FastAPI(lifespan=lifespan)

app.include_router(friend_requests.router)
app.include_router(friends.router)
app.include_router(all_profiles.router)
app.include_router(actions.router)
