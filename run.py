import asyncio

from engine import telegram_bot, dp


async def main():
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
