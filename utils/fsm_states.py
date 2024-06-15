from aiogram.fsm.state import State, StatesGroup


class CreateNotice(StatesGroup):
    get_ticker_name = State()
