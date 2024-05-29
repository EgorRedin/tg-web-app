import asyncio
from bot_web import router
from aiogram import Bot, Dispatcher
from config import config


async def main():
    bot = Bot(config.token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           allowed_updates=["message", "chat_member"])


if __name__ == "__main__":
    asyncio.run(main())
