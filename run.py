import asyncio

from engine import telegram_bot, dp, users_repo


async def main():
    await users_repo.get_all_users_from_db()
    print(users_repo.users)
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
