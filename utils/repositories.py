import time

from utils.models import Session
from utils.patterns import PatternSingleton


class UserRepository(PatternSingleton):
    users: set[int] = set()
    banned_users: set[int] = set()

    def add(self, user_id):
        self.users.add(user_id)

    def delete(self, user_id):
        self.users.discard(user_id)

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass


class SessionRepository(PatternSingleton):
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
