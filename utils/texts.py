def start(name: str):
    return f"<b><u>Привет, {name}!</u></b>"


def ask_ticker():
    return ('<b><u>Выбор тикера для мониторинга</u></b>\n\n'
            'ℹ️ Например BTC или другие.\n'
            'ℹ️ Мониторинг идёт к стейблкоину USDT.\n\n'
            '▶️ <u>Введите название:</u>')


def ask_type_notice(ticker: str, pair: str):
    return (f'<b><u>Мониторинг пары {ticker.upper()}{pair.upper()}</u></b>\n\n'
            f'▶️ <b><u>Выберите тип уведомления:</u></b>')


def ask_period_current_price_percent(current_price: float | str, currency: str):
    return ('<b><u>Уведомление сработает при изменении цены в % от текущей цены до указанного значения %.</u></b>\n\n'
            f'Текущая цена : {current_price} {currency.upper()}\n\n'
            '▶️ <u>Введите процент:</u>')


def ask_values():
    pass
