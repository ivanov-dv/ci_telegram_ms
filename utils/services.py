import httpx

import config
from utils.models import User, UserRequest, UserRequestSchema


class Requests:

    @staticmethod
    async def _send_get(endpoint: str):
        async with httpx.AsyncClient() as client:
            return await client.get(endpoint)

    @staticmethod
    async def _send_post(endpoint: str, data):
        async with httpx.AsyncClient() as client:
            return await client.post(endpoint, data=data)

    @staticmethod
    async def _send_put(endpoint: str, data):
        async with httpx.AsyncClient() as client:
            return await client.put(endpoint, data=data)

    @staticmethod
    async def _send_delete(endpoint: str):
        async with httpx.AsyncClient() as client:
            return await client.delete(endpoint)

    @staticmethod
    async def get_user(user_id: int) -> User:
        response = await Requests._send_get(f'{config.REPO_HOST}/users/{user_id}')
        if response.status_code not in (200, 307):
            response.raise_for_status()
        return User(**response.json())

    @staticmethod
    async def get_all_users() -> dict[int: User]:
        response = await Requests._send_get(f'{config.REPO_HOST}/users/')
        if response.status_code not in (200, 307):
            response.raise_for_status()
        return {user_id: User(**res) for user_id, res in response.json().items()}

    @staticmethod
    async def add_user(user: User) -> User:
        print(user.json())
        response = await Requests._send_post(f'{config.REPO_HOST}/users/', user.json())
        if response.status_code != 201:
            response.raise_for_status()
        return User(**response.json())

    @staticmethod
    async def delete_user(user_id: int):
        response = await Requests._send_delete(f'{config.REPO_HOST}/users/{user_id}')
        if response.status_code != 204:
            response.raise_for_status()
        return response

    @staticmethod
    async def update_user(user: User) -> User:
        response = await Requests._send_put(f'{config.REPO_HOST}/users/{user.user_id}', user.json())
        if response.status_code not in (200, 307):
            response.raise_for_status()
        return User(**response.json())

    @staticmethod
    async def get_request(request_id: int) -> UserRequest:
        response = await Requests._send_get(f'{config.REPO_HOST}/requests/{request_id}')
        if response.status_code not in (200, 307):
            response.raise_for_status()
        return UserRequest(**response.json())

    @staticmethod
    async def get_all_requests_for_user(user_id: int) -> list[UserRequest]:
        response = await Requests._send_get(f'{config.REPO_HOST}/requests/users/{user_id}')
        if response.status_code not in (200, 307):
            response.raise_for_status()
        return [UserRequest(**res) for res in response.json()] if response.json() else None

    @staticmethod
    async def get_all_users_for_request(request_id: int):
        response = await Requests._send_get(f"{config.REPO_HOST}/users/requests/{request_id}")
        if response.status_code not in (200, 307):
            response.raise_for_status()
        return [user_id for user_id in response.json()] if response.json() else None

    @staticmethod
    async def add_request(user_id: int, request: UserRequestSchema):
        response = await Requests._send_post(f"{config.REPO_HOST}/requests/?user_id={user_id}", request.json())
        if response.status_code != 201:
            response.raise_for_status()
        return UserRequest(**response.json()[str(user_id)])

    @staticmethod
    async def delete_request(user_id: int, request_id: int):
        response = await Requests._send_delete(f"{config.REPO_HOST}/requests/{user_id}?request_id={request_id}")
        if response.status_code != 204:
            response.raise_for_status()
        return response

    @staticmethod
    async def get_current_price(ticker: str):
        return await Requests._send_get(f'{config.REPO_HOST}/prices/{ticker}')

    @staticmethod
    async def get_tickers():
        return await Requests._send_get(f'{config.REPO_HOST}/tickers')


# if __name__ == '__main__':
    # pprint(asyncio.run(Requests.get_requests_for_user(182199633)))
    # pprint((asyncio.run(Requests.get_all_users_for_request(1722939704154563840))))
    # user1 = asyncio.run(Requests.get_user(2))
    # print(user1)
    # pprint(asyncio.run(Requests.add_user(user1)))
    # user1.surname = 'test323'
    # pprint(asyncio.run(Requests.update_user(user1)))
    # pprint(asyncio.run(Requests.delete_user(2)))
    # pprint(asyncio.run(Requests.get_user(0)))
    # req = UserRequestSchema.create('BTCUSDT', PercentOfTime(target_percent=30, period=Period.v_24h), Way.up_to)
    # pprint(asyncio.run(Requests.add_request(1, req)))
    # pprint(asyncio.run(Requests.delete_request(1, 1722932008930284032)))
