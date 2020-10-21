from typing import Literal, Optional
from pydantic import validator
from magnet import BaseModel


class RuleAmount(BaseModel):
    target: Literal["order", "wallet"] = "order"
    mode: Literal["rate", "amount", "all"]
    value: float = None  # rate:保有資産のうち何%を配賦するか。 fix:資産関係なく固定値で取引する。


class RulePosition(BaseModel):
    name: str = ""
    description: str = ""
    algorithm: str = "default"
    args: dict = {}
    amount: RuleAmount = None


class RuleTrade(BaseModel):
    entry: RulePosition
    profit: RulePosition = RulePosition(amount=RuleAmount(mode="rate", value=1.4))
    losscut: RulePosition = RulePosition()

    @validator('entry')
    def valid_entry(cls, v: RulePosition, values, **kwargs):
        if v.amount is not None:
            amount = v.amount
            if amount.mode == "rate":
                if amount.value < 0 or 1 < amount.value:
                    raise ValueError("Specify a value between 0 and 1.")
            elif amount.mode == "amount":
                if amount.value < 0:
                    raise ValueError("Specify a value of 0 and more.")
            elif amount.mode == "all":
                if amount.value is not None:
                    raise ValueError("When 'all', Specify a value of None.")
            else:
                raise Exception()

        return v


class TradeSignal(BaseModel):
    id: int
    market: str
    product: str
    periods: int
    amount: float
    broker: str
    signal: Literal["limit_rate", "cross", "arbitrage"]
    previous_order_id: float = None
    limit_rate: float = None  # 前回発注からの変動制限
    request_type: Literal["buy", "sell"]


class TradeProfile(BaseModel):
    class Config:
        orm_mode = True
    id: int
    name: str
    description: str = ""
    provider: str
    market: str
    product: str
    periods: int
    cron: str = ""
    broker: str
    order_id: float = None
    trade_rule: RuleTrade


TradeProfileCreate = TradeProfile.prefab("Create", exclude=["id"])
TradeProfilePatch = TradeProfile.prefab("Patch", optionals=[...])
