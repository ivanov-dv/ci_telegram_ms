import logging
import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


'''
LOGGING LEVEL
'''
LOG_LEVEL = logging.INFO

'''
RabbitMQ
'''
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
RABBITMQ_QUEUE = 'ci_to_telegram'

'''
Telegram API
'''
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_PARSE_MODE = 'HTML'
MAX_SESSION_TIME_SECS = 300


'''
MICROSERVICES_HOSTS
'''
REPO_HOST = os.getenv('REPO_HOST')
BINANCE_HOST = os.getenv('BINANCE_HOST')
