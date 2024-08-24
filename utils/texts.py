from utils.models import UserRequest


def start(name: str):
    return f"<b><u>Привет, {name}!</u></b>"


def ask_ticker():
    return ('<b><u>Выбор тикера для мониторинга</u></b>\n\n'
            'ℹ️ Мониторинг идёт к стейблкоину USDT.\n'
            'ℹ️ <u>Вводить без USDT!</u>\n'
            'ℹ️ Например BTC, ETH или другие.\n\n'
            '▶️ <u>Введите название:</u>')


def ask_type_notice(ticker: str, pair: str, current_price: float):
    return (f'<b><u>Мониторинг пары {ticker.upper()}{pair.upper()}</u></b>\n\n'
            f'Текущая цена: {current_price}\n\n'
            f'▶️ <b><u>Выберите тип уведомления:</u></b>')


def ask_period_current_price_percent(current_price: float | str, currency: str):
    return ('<b><u>Уведомление сработает при изменении цены в % от текущей цены до указанного значения %.</u></b>\n\n'
            f'Текущая цена : {current_price} {currency.upper()}\n\n'
            '▶️ <u>Введите процент:</u>')


def show_notices(data: list[UserRequest] | None):
    if not data:
        return 'У вас нет уведомлений.'
    base = '<b><u>Ваши текущие уведомления:\n\n</u></b>'
    if isinstance(data, list):
        notices = '\n'.join(
            [f'{idx}. {notice}\n---------------------------------' for idx, notice in enumerate(data, start=1)]
        )
        return f'{base}{notices}'
    return 'Invalid text.show_notices'
