from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.assist import get_msg_from_state
from utils.fsm_states import *
from utils.keyboards import *


router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('<b><u>Привет!</u></b>', reply_markup=KB.main())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('<b><u>Привет!</u></b>', reply_markup=KB.main())


@router.callback_query(F.data == 'create_notice')
async def cn_ask_ticker_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNotice.get_ticker_name)
    msg = await callback.message.edit_text(
        '<b><u>Введите название тикера</u></b>',
        reply_markup=CreateNoticeKB.back_to_main())
    await state.update_data({'msg': msg})


@router.message(CreateNotice.get_ticker_name)
async def cn_ask_type_notice(message: types.Message, state: FSMContext):
    await state.update_data({'ticker_name': message.text})
    await message.delete()
    msg = await get_msg_from_state(state)
    await msg.edit_text(
        '<b><u>Выберите тип уведомления</u></b>',
        reply_markup=CreateNoticeKB.type_notice())
    await state.set_state(CreateNotice.set_type_notice)


@router.callback_query(F.data == 'cn_price_up')
async def cn_ask_price_up(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNotice.get_ticker_name)
    msg = await callback.message.edit_text(
        '<b><u>Уведомление сработает при повышении цены до указанного значения.</u></b>\n\n'
        'Введите цену:',
        reply_markup=KB.back_to_main())
    await state.update_data({'type_notice': 'price_up', 'msg': msg})
    await state.set_state(CreateNotice.get_price)


@router.callback_query(F.data == 'cn_price_down')
async def cn_ask_price_down(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNotice.get_ticker_name)
    msg = await callback.message.edit_text(
        '<b><u>Уведомление сработает при снижении цены до указанного значения.</u></b>\n\n'
        'Введите цену:',
        reply_markup=KB.back_to_main())
    await state.update_data({'type_notice': 'price_down', 'msg': msg})
    await state.set_state(CreateNotice.get_price)


@router.callback_query(F.data == 'cn_period_24h')
async def cn_ask_period_24h_percent(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNotice.get_ticker_name)
    msg = await callback.message.edit_text(
        '<b><u>Уведомление сработает при изменении цены в % за последние 24 часа до указанного значения %.</u></b>\n\n'
        'Введите процент:',
        reply_markup=KB.back_to_main())
    await state.update_data({'type_notice': 'period_24h', 'msg': msg})
    await state.set_state(CreateNotice.get_period_24h_percent)


@router.callback_query(F.data == 'cn_period_current_price')
async def cn_ask_period_current_price_percent(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNotice.get_ticker_name)
    msg = await callback.message.edit_text(
        '<b><u>Уведомление сработает при изменении цены в % от текущей цены до указанного значения %.</u></b>\n\n'
        'Введите процент:',
        reply_markup=KB.back_to_main())
    await state.update_data({'type_notice': 'period_current_price', 'msg': msg})
    await state.set_state(CreateNotice.get_period_current_price_percent)


@router.callback_query(F.data == 'cn_period_point')
async def cn_ask_period_point(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(CreateNotice.get_ticker_name)
    msg = await callback.message.edit_text(
        '<b><u>Уведомление сработает при изменении цены в % от указанной цены до указанного значения %.</u></b>\n\n'
        'Введите цену, от которой будет рассчитываться изменение:',
        reply_markup=KB.back_to_main())
    await state.update_data({'type_notice': 'period_point', 'msg': msg})
    await state.set_state(CreateNotice.get_price)


@router.message(CreateNotice.get_price)
async def cn_get_price(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    msg = await get_msg_from_state(state)
    if data['type_notice'] == 'price_up':
        # создание запроса
        await msg.edit_text(
            f'Создано уведомление\n\n'
            f'Уведомлять при\n'
            f'повышении цены\n'
            f'{data["ticker_name"]}\n'
            f'до {message.text}',
            reply_markup=KB.back_to_main())
    if data['type_notice'] == 'price_down':
        # создание запроса
        await msg.edit_text(
            f'Создано уведомление\n\n'
            f'Уведомлять при\n'
            f'снижении цены\n'
            f'{data["ticker_name"]}\n'
            f'до {message.text}',
            reply_markup=KB.back_to_main())
    if data['type_notice'] == 'period_point':
        msg = await msg.edit_text(
            '<b><u>Уведомление сработает при изменении цены в % от указанной цены до указанного значения %.</u></b>\n\n'
            'Введите процент:',
        )
        await state.update_data({'msg': msg})
        await state.set_state(CreateNotice.get_period_point_percent)


@router.message(CreateNotice.get_period_point_percent)
async def cn_get_period_point_percent(message: types.Message, state: FSMContext):
    pass