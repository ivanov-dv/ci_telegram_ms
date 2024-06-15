from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.keyboards import *


router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('<b><u>Привет!</u></b>', reply_markup=KB.test_1())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('<b><u>Привет!</u></b>')
    await callback.answer()
