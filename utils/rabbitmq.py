import aio_pika
import asyncio
import logging

from aio_pika.exceptions import ConnectionClosed

from utils.keyboards import KB


class RabbitMq:
    def __init__(self, bot, repo, user, password, queue_name, host='localhost', port=5672):
        self.bot = bot
        self.repo = repo
        self.user = user
        self.password = password
        self.queue_name = queue_name
        self.host = host
        self.port = port
        self.url = f'amqp://{user}:{password}@{host}:{port}/'
        self.connection = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url, login=self.user, password=self.password)

    async def process_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            user_id, request_message = message.body.decode().split('__')
            await self.bot.send_message(user_id, request_message, reply_markup=KB.remove_notice())

    async def listen_messages(self):
        connection = await aio_pika.connect_robust(self.url, login=self.user, password=self.password)
        print('listen')
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(self.queue_name, durable=True)
        await queue.consume(self.process_message)
        try:
            await asyncio.Future()
        finally:
            await connection.close()

