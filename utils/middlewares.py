from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable
from utils import keyboards as kb


class AuthMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        accounts.update_list_accounts()
        if event.from_user.id in accounts.login_accounts:
            await sessions.update_session(event.from_user.id)
            result = await handler(event, data)
        elif event.from_user.id in accounts.ban_accounts:
            result = await event.answer(f"Ваш аккаунт заблокирован. Обратитесь в поддержку.")
        else:
            result = await event.answer(message_texts.START_TEXT_FOR_NEW_USER,
                                        reply_markup=kb.RegistrationKb().add_registration())
        return result


class AuthCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if event.data == "registration":
            result = await handler(event, data)
        elif event.from_user.id in accounts.login_accounts:
            await sessions.update_session(event.from_user.id)
            result = await handler(event, data)
        elif event.from_user.id in accounts.ban_accounts:
            result = await event.message.edit_text(f"Ваш аккаунт заблокирован. Обратитесь в поддержку.")
        else:
            result = await event.message.edit_text(message_texts.START_TEXT_FOR_NEW_USER,
                                                   reply_markup=kb.RegistrationKb().add_registration())
        return result