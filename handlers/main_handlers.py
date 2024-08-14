import httpx

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


import utils.texts as t

from engine import repo
from utils.fsm_states import CreateRequestFSM
from utils.keyboards import KB, MyRequestsKB


router = Router()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(t.start(message.from_user.first_name), reply_markup=KB.main())


@router.callback_query(F.data == 'start')
async def start_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(t.start(callback.from_user.first_name), reply_markup=KB.main())


@router.callback_query(F.data == 'create_notice')
async def cn_ask_ticker_name(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CreateRequestFSM.get_ticker_name)
    msg = await callback.message.edit_text(t.ask_ticker(), reply_markup=KB.back_to_main())
    await state.update_data({'msg': msg})


@router.callback_query(F.data == 'my_notices')
async def mr_show_requests(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        user_requests = await repo.get_all_requests_for_user(callback.from_user.id)
    except httpx.ConnectError:
        await callback.message.edit_text('Сервис временно недоступен.', reply_markup=KB.main())
    else:
        await state.update_data({'user_requests': user_requests})
        await callback.message.edit_text(t.show_notices(user_requests), reply_markup=MyRequestsKB.my_requests())


@router.callback_query(F.data == 'remove_notice')
async def remove_notice(callback: types.CallbackQuery):
    await callback.message.delete()
