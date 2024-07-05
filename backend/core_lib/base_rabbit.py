from aio_pika import connect_robust, DeliveryMode, Message
from tenacity import retry, stop_after_attempt, wait_exponential


class BaseRabbit:
    @retry(
        stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def __init__(self, RABBITMQ_HOST: str):
        self.RABBITMQ_HOST = RABBITMQ_HOST
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await connect_robust(self.RABBITMQ_HOST)
        self.channel = await self.connection.channel()

    async def ensure_connection(self):
        if self.connection is None or self.connection.is_closed:
            await self.connect()

    async def diconnect(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def publish(self, queue, message, exchange=""):
        await self.ensure_connection()
        await self.channel.declare_queue(queue, durable=True)
        await self.channel.default_exchange.publish(
            Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=queue,
        )

    async def start_consuming(self, queue, no_ack=False):
        await self.ensure_connection()
        queue = await self.channel.declare_queue(queue, durable=True)
        incoming_message = await queue.get(no_ack=no_ack, fail=False)
        if incoming_message:
            return incoming_message
