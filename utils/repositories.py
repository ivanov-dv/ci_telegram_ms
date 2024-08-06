import time

from utils.models import Session, User
from utils.patterns import PatternSingleton
from utils.services import Requests


class UserRepository(PatternSingleton):
    users: set[str] = set()
    banned_users: set[str] = set()

    async def add(self, user: User):
        self.users.add(str(user.user_id))
        await Requests.add_user(user)

    def delete(self, user_id):
        self.users.discard(user_id)

    def get(self, user_id):
        pass

    def update(self, user_id):
        pass

    async def get_all_users_from_db(self):
        users = await Requests.get_all_users()
        self.users = set(users.keys())


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
