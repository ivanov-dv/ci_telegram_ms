from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder


class GeneratorKB:
    pass


class KB:
    b_start = InlineKeyboardButton(text='start', callback_data='start')

    @classmethod
    def test_1(cls):
        return InlineKeyboardBuilder().add(cls.b_start).as_markup()
