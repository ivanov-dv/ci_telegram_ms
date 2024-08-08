import logging
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

import config as cfg

from aiogram import Bot, Dispatcher

from utils.middlewares import AuthMiddleware
from utils.repositories import Repository, SessionRepository

'''
Repositories
'''
repo = Repository()
sessions_repo = SessionRepository()

'''
RabbitMQ
'''
# credentials = pika.PlainCredentials(
#     username=cfg.RABBITMQ_USERNAME,
#     password=cfg.RABBITMQ_PASSWORD,
#     erase_on_connect=True)
# parameters = pika.ConnectionParameters(
#     host=cfg.RABBITMQ_HOST,
#     port=cfg.RABBITMQ_PORT,
#     virtual_host=cfg.RABBITMQ_VHOST,
#     credentials=credentials)
# connection_rabbitmq = pika.BlockingConnection(parameters)


'''
PostgreSQL
'''
# connection_postgres = PostgresDB(
#     username=cfg.POSTGRESQL_USERNAME,
#     password=cfg.POSTGRESQL_PASSWORD,
#     host=cfg.POSTGRESQL_HOST,
#     port=cfg.POSTGRESQL_PORT,
#     database=cfg.POSTGRESQL_DATABASE
# )


'''
Telegram API
'''
telegram_bot = Bot(token=cfg.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=cfg.TELEGRAM_PARSE_MODE))
logging.basicConfig(level=cfg.LOG_LEVEL, stream=sys.stdout)
dp = Dispatcher(storage=MemoryStorage())
outer_middleware = AuthMiddleware(repo, sessions_repo)
dp.message.outer_middleware(outer_middleware)
dp.callback_query.outer_middleware(outer_middleware)
