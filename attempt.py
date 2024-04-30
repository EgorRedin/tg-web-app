from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import queries
router = Router()


@router.message()
async def handle_bank(msg: Message, state: FSMContext):
    await queries.AsyncORM.create_table()
