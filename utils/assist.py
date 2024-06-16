from aiogram import types
from aiogram.fsm.context import FSMContext


async def get_msg_from_state(state: FSMContext) -> types.Message | types.CallbackQuery:
    data = await state.get_data()
    return data['msg']
