import enum
import time

from dataclasses import dataclass, field
from datetime import datetime

from pydantic import BaseModel, Field


class Period(enum.Enum):
    v_4h = "4h"
    v_8h = "8h"
    v_12h = "12h"
    v_24h = "24h"


class Way(enum.Enum):
    up_to = "up_to"
    down_to = "down_to"
    all = "all"


class User(BaseModel):
    user_id: int
    firstname: str
    surname: str
    username: str
    created: datetime
    updated: datetime | None = None
    ban: bool = False

    class Config:
        from_attributes = True

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_id == other.user_id
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.user_id)

    def __repr__(self):
        return (
            f'User(user_id={self.user_id}, firstname="{self.firstname}", surname="{self.surname}", '
            f'username="{self.username}", ban={self.ban}, created={self.created}, updated={self.updated})'
        )

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def create(user_id, firstname, surname, username):
        dt = datetime.utcnow()
        return User(
            user_id=user_id,
            firstname=firstname,
            surname=surname,
            username=username,
            created=dt,
            updated=dt,
            ban=False,
        )


class PercentOfPoint(BaseModel):
    target_percent: float
    current_price: float
    weight: int | None = None
    type_request: str = "percent_of_point"

    def __repr__(self):
        return (
            f"PercentOfPoint(target_percent={self.target_percent}, current_price={self.current_price}, "
            f'weight={self.weight}, type_request="{self.type_request}")'
        )

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.target_percent, self.current_price, self.weight, self.type_request))


class PercentOfTime(BaseModel):
    target_percent: float
    period: Period
    weight: int | None = None
    type_request: str = "percent_of_time"

    def __repr__(self):
        return (
            f"PercentOfTime(target_percent={self.target_percent}, period={self.period}, "
            f'weight={self.weight}, type_request="{self.type_request}")'
        )

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.target_percent, self.period, self.weight, self.type_request))


class Price(BaseModel):
    target_price: float
    weight: int | None = None
    type_request: str = "price"

    def __repr__(self):
        return f'Price(target_price={self.target_price}, weight={self.weight}, type_request="{self.type_request}")'

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash((self.target_price, self.weight, self.type_request))


class UserRequest(BaseModel):
    """
    Класс запросов пользователя.
    Сравнение экземпляров позволяет выявить дубли (время создания и обновления не учитывается).
    """

    request_id: int = Field(default_factory=lambda: int(time.time() * 10 ** 9))
    symbol: str
    request_data: PercentOfTime | PercentOfPoint | Price
    way: Way
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

    def model_post_init(self, __context):
        self.symbol = self.symbol.upper()

    def __eq__(self, other):
        if isinstance(other, UserRequest):
            return (self.symbol, self.request_data, self.way) == (
                other.symbol,
                other.request_data,
                other.way,
            )
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.symbol, self.request_data, self.way))

    def __repr__(self):
        return (
            f"UserRequest(request_id={self.request_id}, symbol='{self.symbol}', "
            f"request_data={self.request_data}, way={self.way}, created={self.created}, updated={self.updated})"
        )

    def __str__(self):
        text = f"<b><u>{self.symbol}</u></b>\n"
        if self.request_data.type_request == 'price':
            if self.way.value == 'up_to':
                text += f"Цена выше {self.request_data.target_price} USDT."
            if self.way.value == 'down_to':
                text += f"Цена ниже {self.request_data.target_price} USDT."
        if self.request_data.type_request == 'percent_of_time':
            if self.request_data.period.value == '24h':
                text += f"Изм цены на {self.request_data.target_percent}% за посл 24ч."
        if self.request_data.type_request == 'percent_of_point':
            text += (f"Изм тек цены на {self.request_data.target_percent}% "
                     f"от цены {self.request_data.current_price} USDT.")
        return text
        # return self.__repr__()

    @staticmethod
    def create(
            symbol: str, request_data: PercentOfTime | PercentOfPoint | Price, way: Way
    ):
        dt = datetime.utcnow()
        return UserRequest(
            symbol=symbol, request_data=request_data, way=way, created=dt, updated=dt
        )


class UserRequestSchema(BaseModel):
    symbol: str
    request_data: PercentOfTime | PercentOfPoint | Price
    way: Way
    created: datetime
    updated: datetime

    @classmethod
    def create(cls, symbol, request_data, way):
        dt = datetime.utcnow()
        return cls(symbol=symbol, request_data=request_data, way=way, created=dt, updated=dt)


@dataclass
class Session:
    user_id: int
    time_update: float = field(default_factory=time.time)
