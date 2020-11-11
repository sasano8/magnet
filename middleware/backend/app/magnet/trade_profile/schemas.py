import datetime
from typing import Literal, Optional
from pydantic import validator, Field
from magnet import BaseModel
from magnet.trade import interface

class RuleAmount(BaseModel):
    target: Literal["order", "wallet"] = "order"
    mode: Literal["rate", "amount", "all"]
    value: float = None  # rate:保有資産のうち何%を配賦するか。 fix:資産関係なく固定値で取引する。


class RulePosition(BaseModel):
    name: str = ""
    description: str = ""
    algorithm: str = "default"
    args: dict = {}
    order_type: Literal["market", "limit"] = "market"  # 指値・成り行き
    time_in_force: Literal['GTC', 'IOC', 'FOK'] = "GTC"
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
    version: int = 0
    name: str
    description: str = ""
    provider: str
    market: str
    product: str
    periods: int
    cron: str = ""
    broker: str
    trade_rule: RuleTrade
    job_type: Literal["production"] = Field("production", const=True)
    trade_type: str = "stop_and_reverse"
    monitor_topic: str = "yesterday_ticker"
    detector_name: str = "detect_t_cross"  # 最終的にはDSLでスクリプト化したい

TradeProfileCreate = TradeProfile.prefab("Create", exclude=["id"])
TradeProfilePatch = TradeProfile.prefab("Patch", optionals=[...])


class TradeJob(TradeProfile):
    job_type: Literal["production", "virtual", "backtest"]
    last_check_date: datetime.datetime = None
    order_status: interface.OrderStatus = None
    # is_backtest: bool = False
    # trade_type: str = "stop_and_reverse"
    # monitor_topic: str = "yesterday_ticker"
    # detector_name: str = "detect_t_cross"  # 最終的にはDSLでスクリプトをコンパイルするようにする

    @property
    def detector(self):
        return self.get_detector_by_name(self.detector_name)

    def get_detector_by_name(self, detector_name):
        if detector_name == "detect_t_cross":
            return self.detect_t_cross
        else:
            raise Exception()

    def detect_t_cross(self, ticker):
        if ticker.t_cross == 0:
            return None
        elif ticker.t_cross == 1:
            return "ask"
        elif ticker.t_cross == -1:
            return "bid"
        else:
            raise Exception()

    @property
    def topic(self):
        return None

    def get_topic_by_name(self, topic_name):
        if topic_name == "yesterday_ticker":
            return None
        else:
            raise Exception()

class TradeResult(BaseModel):
    job_id: int
    order_id: int = None
    msg: str


