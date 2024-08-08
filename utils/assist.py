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


async def check_percent(data: str) -> float | None:
    try:
        return float(data)
    except ValueError:
        return None


async def check_nums_for_delete(data: str) -> list[int] | None:
    try:
        res = list(map(int, data.split()))
    except ValueError:
        return None
    return res
