import attempt
import configurable_doc
import logging
import asyncio
from aiogram import Dispatcher, Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from WalletPay import AsyncWalletPayAPI
import queries
from config_reader import config


router = Router()
api = AsyncWalletPayAPI(api_key=configurable_doc.WALLET_TOKEN)

async def order_handler(order_id: str):
    while True:
        # Get order preview
        order_preview = await api.get_order_preview(order_id=order_id)

        # Check if the order is paid
        if order_preview.status == "PAID":
            print("Order has been paid!")
        else:
            print("Order is not paid yet.")
            await asyncio.sleep(20)


async def main():
    # log
    logging.basicConfig(level=logging.INFO)
    # init
    bot = Bot(token=configurable_doc.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(attempt.router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@router.message(CommandStart())
@router.callback_query(F.data == "main_page")
async def start(message: Message | CallbackQuery):
    await queries.AsyncORM.create_table()
    order = await api.create_order(
        amount=0.01,
        currency_code="TON",
        description="Test Order",
        external_id="1234534536",
        timeout_seconds=1200,
        customer_telegram_user_id=str(message.from_user.id)
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Pay", url=order.direct_pay_link
                )
            ]
        ]
    )
    await message.answer(f'Link: {order.direct_pay_link}', reply_markup = keyboard)
    asyncio.create_task(order_handler(str(order.id)))


if __name__ == '__main__':
    asyncio.run(main())