import time

import config

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

from utils.keyboards import KB
from utils.models import Session, User
from utils.repositories import Repository, SessionRepository


class AuthMiddleware(BaseMiddleware):

    def __init__(self, users_repo: Repository, sessions_repo: SessionRepository):
        self.users_repo = users_repo
        self.sessions_repo = sessions_repo

    async def _check_timeout_session(self, user_id):
        session = await self.sessions_repo.get(user_id)
        res = time.time() - session.time_update
        if res > config.MAX_SESSION_TIME_SECS:
            return True
        return False

    async def session_middleware(self, user_id):
        if user_id in self.sessions_repo.sessions:
            if await self._check_timeout_session(user_id):
                await self.sessions_repo.update(user_id)
                return False
            await self.sessions_repo.update(user_id)
        else:
            await self.sessions_repo.add(Session(user_id))
        return True

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        if str(event.from_user.id) in self.users_repo.users:
            if event.from_user.id in self.users_repo.banned_users:
                return await event.answer("Ваш аккаунт заблокирован. Обратитесь в поддержку.")
        else:
            user = User.create(event.from_user.id, event.from_user.first_name,
                               event.from_user.last_name, event.from_user.username)
            await self.users_repo.add_user(user)
        check_session = await self.session_middleware(event.from_user.id)
        if not check_session:
            if isinstance(event, Message):
                return await event.answer("Ваша сессия истекла, начните заново.")
            if isinstance(event, CallbackQuery):
                return await event.message.edit_text("Ваша сессия истекла, начните заново.",
                                                     reply_markup=KB.back_to_main())
        return await handler(event, data)
