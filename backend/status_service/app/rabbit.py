from os import environ
from json import dumps
from core_lib.base_rabbit import BaseRabbit
from core_lib.schemas import Status

STATUS_QUEUE = environ["STATUS_QUEUE"]
RABBITMQ_HOST = environ["RABBITMQ_HOST"]


class Rabbit(BaseRabbit):
    def __init__(self):
        super().__init__(RABBITMQ_HOST=RABBITMQ_HOST)

    async def publish_status_create_event(self, status: Status):
        status_message = Status(username=status.username, status=status.status)
        await self.publish(
            exchange="",
            queue=STATUS_QUEUE,
            message=dumps(status_message, default=vars),
        )
