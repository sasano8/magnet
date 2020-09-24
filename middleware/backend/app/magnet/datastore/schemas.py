from pydantic import BaseModel
import datetime
from typing import Optional

class Ohlc(BaseModel):
    id: Optional[int]
    market: str
    product: str
    close_time: datetime.datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    quote_volume: float

    class Config:
        orm_mode = True

