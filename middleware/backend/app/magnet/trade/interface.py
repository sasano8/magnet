import datetime
from typing import Literal, Union
from pydantic import validator, root_validator, Field
from magnet import BaseModel
from magnet.vendors import funnel


class Order(BaseModel):
    order_date: datetime.datetime = None
    result_info: dict = None
    bid_or_ask: Literal["ask", "bid"]
    order_type: Literal["market", "limit"] = "market"
    time_in_force: Literal['GTC', 'IOC', 'FOK'] = "GTC"
    currency_pair: str
    price: float = None
    amount: float = 0
    limit: float = None
    comment: str = None
    reason: str = ""
    sys_comment: str = "テスト中"

    @property
    def is_done(self) -> bool:
        return self._is_done(self.order_date, self.result_info)

    @classmethod
    def _is_done(cls, order_date, result_info):
        if order_date is None and result_info is None:
            result = False
        elif order_date is not None and result_info is not None:
            result = True
        else:
            raise ValueError()
        return result

    @root_validator()
    def valid_status(cls, values):
        order_date = values.get("order_date", None)
        result_info = values.get("result_info", None)
        cls._is_done(order_date, result_info)
        return values

    def get_invert_bid_or_ask(self) -> str:
        if self.bid_or_ask == "ask":
            return "bid"
        elif self.bid_or_ask == "bid":
            return "ask"
        else:
            raise Exception()


class OrderResult(Order):
    order_date: datetime.datetime
    result_info: dict
    price: float = None  # 約定時の平均価格
    # exec_amount: float = None
    exec_price: float = None  # amountを計算した実質の約定金額
    commission: float = None


class OrderStatus(BaseModel):
    schema_version: int = Field(0, const=True)
    last_order_date: datetime.datetime = None
    entry_order: Union[Order, OrderResult]
    settle_order: Union[Order, OrderResult]

    def __init__(self, **kwargs):
        # e = kwargs["entry_order"]
        # s = kwargs["settle_order"]
        kwargs.pop("last_check_date", None)

        # for x in [e, s]:
        #     if hasattr(x, "commission_rate"):
        #         delattr(x, "commission_rate")

        super().__init__(**kwargs)

    @property
    def status(self) -> Literal["ready", "entried", "settled"]:
        e_is_done = self.entry_order.is_done
        s_is_done = self.settle_order.is_done

        if e_is_done is None or s_is_done is None:
            raise Exception("There can be no situation where return None.")

        if not e_is_done and s_is_done:
            raise Exception("There can be no situation where payment is made without entry.")

        if not e_is_done:
            result = "ready"
        elif e_is_done:
            if not s_is_done:
                result = "entried"
            elif s_is_done:
                result = "settled"
            else:
                raise ValueError()
        else:
            raise ValueError()

        return result

    @staticmethod
    def create_settle_order(entry_order: Order) -> Order:
        """反対売買のためのorderを作成する"""
        order = entry_order.copy(deep=True)
        order.bid_or_ask = order.get_invert_bid_or_ask()
        return order


class BrokerBase:
    @property
    def __name__(self):
        return self.__class__.__name__.lower()

    @staticmethod
    def valid_currency_pair(currency_pair: str) -> bool:
        raise NotImplementedError()

    @staticmethod
    def map_currency_pair(currency_pair: str) -> str:
        raise NotImplementedError()

    async def get_ticker(self, currency_pair: str):
        raise NotImplementedError()

    @funnel
    async def post_order(self, order: Order) -> Order:
        raise NotImplementedError()

    @funnel
    async def fetch_order_result(self, order: Order) -> OrderResult:
        raise NotImplementedError()

    async def order(self, entry_or_settle_or_dummy, profile, close_time_or_every_second, db):
        profile = profile.copy(deep=True)
        if entry_or_settle_or_dummy == "entry":
            order_result = await self.post_order(profile.order_status.entry_order)
            profile.order_status.entry_order = order_result
            profile.order_status.last_order_date = order_result.order_date
            profile.last_check_date = close_time_or_every_second
        elif entry_or_settle_or_dummy == "settle":
            order_result = await self.post_order(profile.order_status.settle_order)
            profile.order_status.settle_order = order_result
            profile.order_status.last_order_date = order_result.order_date
            profile.last_check_date = close_time_or_every_second
        elif entry_or_settle_or_dummy == "pass":
            profile.last_check_date = close_time_or_every_second
        else:
            raise Exception()
        from magnet import get_db
        from magnet.trade_profile.schemas import TradeJob
        from magnet.trade_profile.crud import TradeJob as TradeJobCrud
        # for db in get_db():
        crud = TradeJobCrud(db)
        result = crud.update(data=profile)

        return TradeJob.from_orm(result)

    async def get_topic(self, db, job, close_time_or_every_second):
        import magnet.datastore.crud
        ohlc = magnet.datastore.crud.CryptoOhlcDaily(db)
        result = ohlc.get_ticker(
            provider=job.provider,
            market=job.market,
            product=job.product,
            periods=job.periods,
            close_time=close_time_or_every_second
        )
        return result

    def detect_signal(self, ticker) -> Union[Literal["ask", "bid"], None]:
        # サイン検出
        if ticker.t_cross == 0:
            return None
        elif ticker.t_cross == 1:
            return "ask"
        elif ticker.t_cross == -1:
            return "bid"
        else:
            raise Exception()

    def detect_limit_signal(self) -> bool:
        return False


