import asyncio

import sentry_sdk

from config import SENTRY_DSN
from engine import telegram_bot, dp, repo, rabbit
from handlers import main_handlers, create_notice, my_requests


async def main_bot():
    dp.include_routers(
        main_handlers.router,
        create_notice.router,
        my_requests.router,
    )
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


async def main():
    await asyncio.sleep(10)
    await asyncio.gather(
        main_bot(),
        repo.get_tickers(),
        rabbit.listen_messages(),
        repo.load_users_from_db()
    )


if __name__ == "__main__":
    if SENTRY_DSN:
        sentry_sdk.init(SENTRY_DSN)
    asyncio.run(main())
