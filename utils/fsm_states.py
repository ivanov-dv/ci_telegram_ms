from aiogram.fsm.state import State, StatesGroup


class CreateNotice(StatesGroup):
    set_type_notice = State()
    get_ticker_name = State()
    get_price = State()
    get_period_24h_percent = State()
    get_period_current_price_percent = State()
    get_period_point = State()
    get_period_point_percent = State()
