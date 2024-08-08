from aiogram.fsm.state import State, StatesGroup


class CreateRequestFSM(StatesGroup):
    set_type_request = State()
    get_ticker_name = State()
    get_price = State()
    get_period_24h_percent = State()
    get_period_current_price_percent = State()
    get_period_point = State()
    get_period_point_percent = State()


class MyRequestsFSM(StatesGroup):
    show_requests = State()
    delete_requests = State()
