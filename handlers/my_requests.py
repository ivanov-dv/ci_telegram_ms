from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from engine import repo
from utils import texts as t
from utils.assist import get_msg_from_state, check_nums_for_delete
from utils.fsm_states import MyRequestsFSM
from utils.keyboards import MyRequestsKB, KB

router = Router()


@router.callback_query(F.data == 'mr_delete')
async def mr_ask_nums_requests_for_delete(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        user_requests = data['user_requests']
    except KeyError:
        await callback.message.edit_text('Ошибка получения списка уведомлений.\n'
                                         'Попробуйте повторно',
                                         reply_markup=KB.back_to_main())
    else:
        msg = await callback.message.edit_text(
            f'{t.show_notices(user_requests)}\n\n'
            f'Введите номер запроса или несколько номеров через пробел для удаления\n'
            'Например "2" или "2 3 5"\n',
            reply_markup=MyRequestsKB.back_to_my_requests()
        )
        await state.update_data({'msg': msg})
        await state.set_state(MyRequestsFSM.delete_requests)


@router.message(MyRequestsFSM.delete_requests)
async def mr_get_nums_requests_and_delete(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    msg = await get_msg_from_state(state)
    try:
        user_requests = data['user_requests']
    except KeyError:
        await msg.edit_text('Ошибка получения списка уведомлений.'
                            'Попробуйте повторно',
                            reply_markup=KB.back_to_main())
    else:
        if not user_requests:
            await msg.edit_text('У вас нет уведомлений.', reply_markup=KB.back_to_main())
            return
        nums_for_delete = await check_nums_for_delete(message.text)
        if not nums_for_delete:
            await msg.edit_text('Некорректные данные.\n'
                                'Необходимо ввести номер запроса или несколько номеров через пробел.\n'
                                'Например "2" или "2 3 5"\n'
                                'Попробуйте еще раз.',
                                reply_markup=MyRequestsKB.back_to_my_requests())
        del_list = []
        for req_number in nums_for_delete:
            request_for_delete = user_requests[req_number - 1]
            try:
                await repo.delete_request_for_user(message.from_user.id, request_for_delete.request_id)
                del_list.append(f'№_{req_number}')
            except Exception as e:
                await msg.edit_text(f'Ошибка удаления уведомления с номером {req_number}: {e}',
                                    reply_markup=MyRequestsKB.back_to_my_requests())
        await msg.edit_text(f'Уведомления {", ".join(del_list)} удалены.',
                            reply_markup=MyRequestsKB.back_to_my_requests())


@router.callback_query(F.data == 'mr_delete_all')
async def mr_delete_all(callback: types.CallbackQuery):
    try:
        await repo.delete_all_requests_for_user(callback.from_user.id)
        await callback.message.edit_text('Все уведомления удалены.', reply_markup=MyRequestsKB.back_to_my_requests())
    except Exception as e:
        await callback.message.edit_text(f'Ошибка удаления: {e}', reply_markup=MyRequestsKB.back_to_my_requests())
