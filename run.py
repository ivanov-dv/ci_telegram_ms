import asyncio
import logging

from engine import telegram_bot, dp, repo
from handlers import main_handlers, create_notice, my_requests


async def main():
    dp.include_routers(
        main_handlers.router,
        create_notice.router,
        my_requests.router,
    )
    try:
        await repo.get_all_users_from_db()
    except Exception as e:
        logging.error(f'Error getting users from database: {e}')
    asyncio.create_task(repo.get_tickers())
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
