import config


from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

from utils.models import *
from utils.repositories import UserRepository, SessionRepository


class AuthMiddleware(BaseMiddleware):

    def __init__(self, users_repo: UserRepository, sessions_repo: SessionRepository):
        self.users_repo = users_repo
        self.sessions_repo = sessions_repo

    def _check_timeout_session(self, user_id):
        session = self.sessions_repo.get(user_id)
        res = time.time() - session.time_update
        if res > config.MAX_SESSION_TIME_SECS:
            return True
        return False

    def session_middleware(self, user_id):
        if user_id in self.sessions_repo.sessions:
            if self._check_timeout_session(user_id):
                self.sessions_repo.update(user_id)
                return False
            self.sessions_repo.update(user_id)
        else:
            self.sessions_repo.add(Session(user_id))
        return True

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id in self.users_repo.users:
            if self.users_repo.get(event.from_user.id).ban:
                return await event.answer("Ваш аккаунт заблокирован. Обратитесь в поддержку.")
        else:
            self.users_repo.add(
                User(
                    event.from_user.id,
                    event.from_user.first_name,
                    event.from_user.last_name,
                    event.from_user.username,
                    dt.utcnow(),
                    dt.utcnow(),
                )
            )
        check_session = self.session_middleware(event.from_user.id)
        if not check_session:
            if isinstance(event, Message):
                return await event.answer("Ваша сессия истекла, начните заново.")
            if isinstance(event, CallbackQuery):
                return await event.message.edit_text("Ваша сессия истекла, начните заново.")
        return await handler(event, data)
