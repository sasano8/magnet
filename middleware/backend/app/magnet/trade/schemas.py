from pydantic import BaseModel
from typing import List, Set, Any


class ProfilePrimitive(BaseModel):
    name: str
    position_ratio: float = 0.015  # ポジションを持つ乖離率
    limit_ratio: float = 0.015 /1.8 # ポジションを解消する乖離率
    strategy: str
    coin: str
    markets: Set[str]


class Profile(ProfilePrimitive):
    strategy: str
    coin: str
    markets: Set[str]


class Strategy(BaseModel):
    exchanges: Set[Any]


