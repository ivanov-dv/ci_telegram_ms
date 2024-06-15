import threading

import config


from typing_extensions import Self

from utils.models import *
from utils.patterns import PatternSingleton, RepositoryDB


class UserRepository(RepositoryDB, PatternSingleton):
    users: dict[int, User] = {}

    def add(self, user: User) -> None:
        self.users[user.user_id] = user

    def delete(self, user: User) -> None:
        if self.users.get(user.user_id, None):
            self.users.pop(user.user_id)

    def get(self, user_id: int) -> User:
        return self.users.get(user_id, None)

    def update(self, user: User) -> None:
        if self.users.get(user.user_id, None):
            self.users[user.user_id] = user


class SessionRepository(RepositoryDB, PatternSingleton):
    sessions: dict[int, Session] = {}

    def add(self, session: Session) -> None:
        self.sessions[session.user_id] = session

    def delete(self, user_id: int) -> None:
        if self.sessions.get(user_id, None):
            self.sessions.pop(user_id)

    def get(self, user_id) -> Session:
        return self.sessions.get(user_id, None)

    def update(self, user_id) -> None:
        self.sessions[user_id].time_update = time.time()


class RequestRepository(RepositoryDB, PatternSingleton):
    user_requests: dict[int, set[UserRequest]] = {}
    unique_user_requests: dict[UserRequest, set[int]] = {}
    unique_requests_for_server: set[RequestForServer] = set()

    def _delete_unique_user_request(self, user_id: int, request: UserRequest) -> None:
        if request in self.unique_user_requests:
            self.unique_user_requests[request].discard(user_id)
            if not self.unique_user_requests[request]:
                self.unique_user_requests.pop(request, None)

    def add(self, user_id: int, request: UserRequest) -> Self:

        if user_id in self.user_requests:
            self.user_requests[user_id].add(request)
        else:
            self.user_requests.update({user_id: {request}})

        if request in self.unique_user_requests:
            self.unique_user_requests[request].add(user_id)
        else:
            self.unique_user_requests.update({request: {user_id}})

        return self

    def delete(self, user_id: int, request: UserRequest) -> Self:
        if user_id in self.user_requests:
            self.user_requests[user_id].discard(request)
            if not self.user_requests[user_id]:
                self.user_requests.pop(user_id, None)
        self._delete_unique_user_request(user_id, request)
        return self

    def update_time_request(self, user_id: int, request: UserRequest) -> Self:
        """
        Обновляет время изменения запроса.
        """

        list_requests = list(self.user_requests[user_id])
        list_requests[list_requests.index(request)].time_info.update_time = dt.utcnow()
        list_requests[list_requests.index(request)].time_info.update_time_unix = time.time()
        self.user_requests[user_id] = set(list_requests)
        return self

    def get(self, user_id: int, request: UserRequest) -> UserRequest | None:
        return request if user_id in self.user_requests and request in self.user_requests[user_id] else None

    def get_all_for_user_id(self, user_id: int) -> set[UserRequest] | None:
        return self.user_requests[user_id] if user_id in self.user_requests else None

    def do_unique_requests_for_server(self) -> set[RequestForServer]:
        """
        Создает словарь с уникальными запросами (без дублей) на API.
        Сортирует запросы по ключам TypeRequest.percent и TypedRequest.price.

        :return: Set[RequestForServer]
        """

        self.unique_requests_for_server = set(map(RequestForServer, self.unique_user_requests.keys()))

        return self.unique_requests_for_server
