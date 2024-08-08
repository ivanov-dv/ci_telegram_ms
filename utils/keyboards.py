from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder


class GeneratorKB:
    pass


class KB:
    b_back_to_main = InlineKeyboardButton(text='На главную', callback_data='start')
    b_create_notice = InlineKeyboardButton(text='Создать уведомление', callback_data='create_notice')
    b_my_notices = InlineKeyboardButton(text='Мои уведомления', callback_data='my_notices')

    @classmethod
    def main(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_create_notice, cls.b_my_notices)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_main(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_main)
        return builder.as_markup()


class CreateNoticeKB(KB):
    b_price_up = InlineKeyboardButton(
        text='Повышение цены до', callback_data='cn_price_up')
    b_price_down = InlineKeyboardButton(
        text='Снижение цены до', callback_data='cn_price_down')
    b_period_24h = InlineKeyboardButton(
        text='Изменение в % за 24ч', callback_data='cn_period_24h')
    b_period_current_price = InlineKeyboardButton(
        text='Изменение в % от текущей цены', callback_data='cn_period_current_price')
    b_period_point = InlineKeyboardButton(
        text='Изменение в % от указанной цены', callback_data='cn_period_point')

    @classmethod
    def type_notice(cls):
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_price_up,
            cls.b_price_down,
            cls.b_period_24h,
            cls.b_period_current_price,
            cls.b_period_point,
            cls.b_back_to_main)
        return builder.adjust(1).as_markup()


class MyRequestsKB(KB):
    b_delete = InlineKeyboardButton(
        text='Выбрать и удалить', callback_data='mr_delete')
    b_delete_all = InlineKeyboardButton(
        text='Удалить все', callback_data='mr_delete_all')
    b_back_to_my_requests = InlineKeyboardButton(
        text='В мои уведомления', callback_data='my_notices')

    @classmethod
    def my_requests(cls):
        builder = InlineKeyboardBuilder()
        builder.add(
            cls.b_delete,
            cls.b_delete_all,
            cls.b_back_to_main)
        return builder.adjust(1).as_markup()

    @classmethod
    def back_to_my_requests(cls):
        builder = InlineKeyboardBuilder()
        builder.add(cls.b_back_to_my_requests)
        return builder.adjust(1).as_markup()
