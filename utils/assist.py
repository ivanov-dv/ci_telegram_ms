from aiogram import types
from aiogram.fsm.context import FSMContext


async def get_msg_from_state(state: FSMContext) -> types.Message | types.CallbackQuery:
    data = await state.get_data()
    return data['msg']


async def check_price(data: str) -> float | None:
    try:
        return float(data)
    except ValueError:
        return None

