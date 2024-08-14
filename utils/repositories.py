import asyncio
import time

import httpx

from utils.models import Session, User
from utils.patterns import PatternSingleton
from utils.services import Requests


class Repository(PatternSingleton):
    users: set[str] = set()
    banned_users: set[str] = set()
    tickers: set[str] = set()

    async def add_user(self, user: User) -> User:
        res = await Requests.add_user(user)
        self.users.add(str(user.user_id))
        return res

    async def delete_user(self, user_id: int):
        res = await Requests.delete_user(user_id)
        self.users.discard(str(user_id))
        return res

    async def get_user(self, user_id: int) -> User | None:
        if str(user_id) not in self.users:
            return None
        return await Requests.get_user(user_id)

    async def update_user(self, user: User) -> User | None:
        if str(user.user_id) not in self.users:
            return None
        return await Requests.update_user(user)

    async def get_all_users_from_db(self):
        users = await Requests.get_all_users()
        self.users = set(users.keys())

    @staticmethod
    async def get_request(request_id: int):
        return await Requests.get_request(request_id)

    @staticmethod
    async def get_all_requests_for_user(user_id: int):
        return await Requests.get_all_requests_for_user(user_id)

    @staticmethod
    async def get_all_users_for_request(request_id: int):
        return await Requests.get_all_users_for_request(request_id)

    @staticmethod
    async def delete_request_for_user(user_id: int, request_id: int):
        await Requests.delete_request(user_id, request_id)

    @staticmethod
    async def delete_all_requests_for_user(user_id: int) -> None:
        user_requests = await Requests.get_all_requests_for_user(user_id)
        if not user_requests:
            return
        for req in user_requests:
            await Requests.delete_request(user_id, req.request_id)

    async def get_tickers(self) -> None:
        while True:
            try:
                res = await Requests.get_tickers()
            except httpx.ConnectError:
                print('Ошибка получения списка торговых пар')
                await asyncio.sleep(10)
            else:
                self.tickers = set(res)
                print('Список пар обновлен')
                await asyncio.sleep(86400)

    @staticmethod
    async def get_current_price(ticker: str) -> float:
        return await Requests.get_current_price(ticker)


class SessionRepository(PatternSingleton):
    sessions: dict[int, Session] = {}

    async def add(self, session: Session) -> None:
        self.sessions[session.user_id] = session

    async def delete(self, user_id: int) -> None:
        if self.sessions.get(user_id, None):
            self.sessions.pop(user_id)

    async def get(self, user_id) -> Session:
        return self.sessions.get(user_id, None)

    async def update(self, user_id) -> None:
        self.sessions[user_id].time_update = time.time()
