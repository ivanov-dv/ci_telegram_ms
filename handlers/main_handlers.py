from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.fsm_states import *
from utils.keyboards import *


router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('<b><u>Привет!</u></b>', reply_markup=KB.main())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('<b><u>Привет!</u></b>', reply_markup=KB.main())


@router.callback_query(F.data == 'create_notice')
async def create_notice_callback(callback: types.CallbackQuery, state: FSMContext):
    msg = await callback.message.edit_text('<b><u>Введите торговую пару:</u></b>', reply_markup=KB.back_to_main())
    await state.set_state(CreateNotice.get_ticker_name)
    await state.update_data({'msg': msg})


@router.message(CreateNotice.get_ticker_name)
async def set_params(message: types.Message, state: FSMContext):
    await state.update_data({'ticker_name': message.text})
    await message.delete()
    data = await state.get_data()
    msg = data['msg']
    await msg.edit_text('123', reply_markup=KB.back_to_main())
