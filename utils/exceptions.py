class UserNotFound(Exception):
    def __init__(self, user_id, code=None):
        self.message = f"User ID <{user_id}> not found. "
        if code:
            self.message += f"HTTP status code: {code}"

    def __str__(self):
        return self.message


class UnprocessableEntity(Exception):
    pass
