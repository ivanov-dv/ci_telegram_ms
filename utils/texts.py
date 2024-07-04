def start(name):
    return f"<b><u>Привет, {name}!</u></b>"


def ask_ticker():
    return (f'<b><u>Название тикера для мониторинга</u></b>\n\n'
            f'ℹ️ Например BTC или другие.\n'
            f'ℹ️ Мониторинг идёт к стейблкоину USDT.\n\n'
            f'▶️ <u>Введите название:</u>')


def ask_type_notice(ticker):
    return (f'<b><u>Мониторинг пары {ticker}</u></b>\n\n'
            f'▶️ <b><u>Выберите тип уведомления</u></b>')
