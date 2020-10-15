from pydantic import BaseModel
import datetime
from typing import Optional, List, Iterable
from libs.linq import Linq


class Ohlc(BaseModel):
    id: Optional[int]
    provider: str
    market: str
    product: str
    periods: int
    close_time: datetime.datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    quote_volume: float

    t_sma_5: float = None
    t_sma_10: float = None
    t_sma_15: float = None
    t_sma_20: float = None
    t_sma_25: float = None
    t_sma_30: float = None
    t_sma_200: float = None

    t_cross: float = None

    class Config:
        orm_mode = True

    @classmethod
    def compute_technical(cls, ohlc_arr: Iterable["Ohlc"]):
        import pandas as pd

        ohlc_arr = list(ohlc_arr)
        sr = Linq(ohlc_arr).map(lambda x: x.close_price).series()

        # sr = pd.Series(map(ohlc_arr, lambda x: x.close_price))
        sma_5 = sr.rolling(5, min_periods=1).mean()  # 一週間　仮想通貨の場合は？？
        sma_10 = sr.rolling(10, min_periods=1).mean()
        sma_15 = sr.rolling(15, min_periods=1).mean()
        sma_20 = sr.rolling(20, min_periods=1).mean()
        sma_25 = sr.rolling(25, min_periods=1).mean()
        sma_30 = sr.rolling(30, min_periods=1).mean()
        sma_200 = sr.rolling(200, min_periods=1).mean()  # 取引所の年間営業日が200日程度

        for index, item in enumerate(ohlc_arr):
            item.t_sma_5 = sma_5[index]
            item.t_sma_10 = sma_10[index]
            item.t_sma_15 = sma_15[index]
            item.t_sma_20 = sma_20[index]
            item.t_sma_25 = sma_25[index]
            item.t_sma_30 = sma_30[index]
            item.t_sma_200 = sma_200[index]

            # ゴールデンクロス・デッドクロス検知
            if item.t_sma_5 > item.t_sma_25:
                item.t_cross = 1
            elif item.t_sma_5 < item.t_sma_25:
                item.t_cross = -1
            else:
                item.t_cross = 0

        previous_cross = 0

        for item in ohlc_arr:
            if previous_cross == item.t_cross:
                previous_cross = item.t_cross
                item.t_cross = 0

            else:
                previous_cross = item.t_cross

        return ohlc_arr


class Detail(BaseModel):
    url: Optional[str]
    url_cache: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    class Config:
        extra = "allow"


class CommonSchema(BaseModel):
    # Config = ORM
    class Config:
        orm_mode = True

    # pipeline: str
    # crawler_name: str
    # keyword: str
    # option_keywords: List[str] = []
    # deps: int = 0
    referer: Optional[str]
    url: Optional[str]
    url_cache: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    detail: Detail = Detail()

    def copy_summary(self):
        dic = self.dict(exclude={"detail"})
        obj = self.__class__.construct(**dic)
        return obj

    def sync_summary_from_detail(self):
        self.url = self.detail.url
        self.url_cache = self.detail.url_cache
        self.title = self.detail.title
        self.summary = self.detail.summary