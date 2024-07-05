from os import environ
from json import loads
import asyncio
from aio_pika import IncomingMessage
from core_lib.base_rabbit import BaseRabbit
from core_lib.models import Notification, StatusNotification
from core_lib.schemas import StatusDTO
from dependencies import get_friends_for_user

STATUS_QUEUE = environ["STATUS_QUEUE"]
NOTIFICATION_QUEUE = environ["NOTIFICATION_QUEUE"]
RABBITMQ_HOST = environ["RABBITMQ_HOST"]


class Rabbit(BaseRabbit):
    def __init__(self):
        super().__init__(RABBITMQ_HOST=RABBITMQ_HOST)

    async def send_notification(self, notification: Notification):
        await super().publish(
            exchange="",
            queue=NOTIFICATION_QUEUE,
            message=notification.model_dump_json(),
        )

    async def notify_friends(self, message: IncomingMessage):
        status_message = StatusDTO(**loads(message.body))
        username = status_message.username
        friends = await get_friends_for_user(username)
        for friend_username in friends:
            await self.send_notification(
                notification=StatusNotification(
                    receiver_username=friend_username,
                    username=status_message.username,
                    status=status_message.status,
                )
            )
        await message.ack()

    async def start_consuming(self):
        while True:
            message = await super().start_consuming(queue=STATUS_QUEUE)
            if message:
                await self.notify_friends(message)
            await asyncio.sleep(1)
