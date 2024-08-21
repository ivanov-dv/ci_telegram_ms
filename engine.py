import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


import config as cfg

from utils.middlewares import AuthMiddleware
from utils.rabbitmq import RabbitMq
from utils.repositories import Repository, SessionRepository

'''
Repositories
'''
repo = Repository()
sessions_repo = SessionRepository()


'''
Telegram API
'''
telegram_bot = Bot(token=cfg.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=cfg.TELEGRAM_PARSE_MODE))
logging.basicConfig(level=cfg.LOG_LEVEL, stream=sys.stdout)
dp = Dispatcher(storage=MemoryStorage())
middleware = AuthMiddleware(repo, sessions_repo)


'''
RabbitMQ
'''
rabbit = RabbitMq(telegram_bot, repo, cfg.RABBITMQ_USER, cfg.RABBITMQ_PASSWORD,
                  cfg.RABBITMQ_QUEUE, cfg.RABBITMQ_HOST, cfg.RABBITMQ_PORT)
