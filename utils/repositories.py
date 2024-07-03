from typing_extensions import Self

from utils.models import *
from utils.patterns import PatternSingleton, RepositoryDB


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
