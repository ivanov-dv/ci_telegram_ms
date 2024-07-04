import datetime
import enum
import time

from dataclasses import dataclass, field
from datetime import datetime as dt

from pydantic import BaseModel

import config


class Period(enum.Enum):
    v_4h = '4h'
    v_8h = '8h'
    v_12h = '12h'
    v_24h = '24h'


class TypeRequest(enum.Enum):
    period = 'period'
    price = 'price'


class Way(enum.Enum):
    up_to = 'up_to'
    down_to = 'down_to'
    all = 'all'


@dataclass(frozen=True)
class Percent:
    target_percent: float


@dataclass(frozen=True)
class PercentOfPoint(Percent):
    current_price: float

    def to_dict(self):
        return {'type': 'percent_of_point', 'target_percent': self.target_percent, 'current_price': self.current_price}


@dataclass(frozen=True)
class PercentOfTime(Percent):
    period: Period

    def to_dict(self):
        return {'type': 'percent_of_time', 'target_percent': self.target_percent, 'period': self.period.value}


@dataclass(frozen=True)
class Price:
    target_price: float

    def to_dict(self):
        return {'type': 'price', 'target_price': self.target_price}


@dataclass
class TimeInfo:
    create_time: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    update_time: datetime.datetime = None
    create_time_unix: float = field(default_factory=time.time)
    update_time_unix: float = None

    def __post_init__(self):
        self.update_time = self.create_time
        self.update_time_unix = self.create_time_unix


@dataclass(repr=False, eq=False, order=False)
class Symbol:
    symbol: str

    def __post_init__(self):
        self.symbol = self.symbol.upper()

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.symbol == other.symbol
        if isinstance(other, str):
            return self.symbol == other

    def __ne__(self, other):
        if isinstance(other, Symbol):
            return self.symbol != other.symbol
        if isinstance(other, str):
            return self.symbol != other

    def __hash__(self):
        return hash(self.symbol)


class User(BaseModel):
    user_id: int
    firstname: str
    surname: str
    username: str
    date_registration: datetime.datetime = dt.utcnow()
    date_update: datetime.datetime = dt.utcnow()
    ban: bool = False

    def __eq__(self, other):
        if isinstance(other, User):
            return self.user_id == other.user_id
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.user_id)

# @dataclass
# class User:
#     user_id: int
#     firstname: str
#     surname: str
#     username: str
#     date_registration: datetime.datetime = dt.utcnow()
#     date_update: datetime.datetime = dt.utcnow()
#     ban: bool = False
#
#     def to_dict(self):
#         return {
#             'user_id': self.user_id,
#             'firstname': self.firstname,
#             'surname': self.surname,
#             'username': self.username,
#             'date_registration': repr(self.date_registration),
#             'date_update': repr(self.date_update),
#             'ban': self.ban
#         }
#
#     def from_dict(self, data):
#         pass


@dataclass
class Session:
    user_id: int
    time_update: float = field(default_factory=time.time)


@dataclass
class BaseRequest:
    request_id: int = field(
        default_factory=lambda: int(time.time() * 10**9),
        init=False
    )


@dataclass(eq=False, order=False)
class UserRequest(BaseRequest):
    """
    Класс запросов пользователя.
    Сравнение экземпляров позволяет выявить дубли (время создания и обновления не учитывается).
    """

    symbol: Symbol
    data_request: PercentOfTime | PercentOfPoint | Price
    way: Way
    time_info: TimeInfo = field(default_factory=TimeInfo, init=False)

    def __eq__(self, other):
        if isinstance(other, UserRequest):
            return (self.symbol, self.data_request, self.way) == (other.symbol, other.data_request, other.way)
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.symbol, self.data_request, self.way))

    def to_dict(self):
        return {
            'id': self.request_id,
            'symbol': self.symbol.symbol,
            'way': self.way.value,
            'data_request': self.data_request.to_dict()
        }
