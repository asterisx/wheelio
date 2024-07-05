from os import environ
from core_lib.base_rabbit import BaseRabbit

NOTIFICATION_QUEUE = environ["NOTIFICATION_QUEUE"]
RABBITMQ_HOST = environ["RABBITMQ_HOST"]


class Rabbit(BaseRabbit):
    def __init__(self):
        super().__init__(RABBITMQ_HOST=RABBITMQ_HOST)

    async def start_consuming(self):
        return await super().start_consuming(queue=NOTIFICATION_QUEUE)
