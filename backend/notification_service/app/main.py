from json import loads
from typing import Optional
from asyncio import sleep
from fastapi import FastAPI, Header
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from aio_pika import IncomingMessage
from core_lib.consul import register_service
from core_lib.models import Notification, NotificationWrapper
from core_lib.values import OPENAPI_EXTRA_PROTECTED
from rabbit import Rabbit

app = FastAPI()


register_service()

user_message_queue = {}


class SSEMessage(BaseModel):
    data: Notification


@app.get("/", response_model=SSEMessage, openapi_extra=OPENAPI_EXTRA_PROTECTED)
async def sse_endpoint(
    current_user_name: str = Header(
        alias="X-Current-User-Name", include_in_schema=False
    ),
):
    print(f"SSE connection established for user: {current_user_name}")
    rabbit = Rabbit()

    await rabbit.connect()

    async def event_generator():
        print("Event generator started", current_user_name)
        while True:
            await sleep(1)
            try:
                message: Optional[IncomingMessage] = await rabbit.start_consuming()
                if message:
                    notification = NotificationWrapper.parse(
                        loads(message.body.decode())
                    )
                    if notification.receiver_username != current_user_name:
                        await rabbit.publish(message=message.body.decode())
                    else:
                        await message.ack()
                        yield notification.model_dump_json()
            except Exception as e:
                print(f"Error while consuming message: {e}")

    return EventSourceResponse(event_generator(), media_type="text/event-stream")
