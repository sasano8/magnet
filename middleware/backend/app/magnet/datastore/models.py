from magnet.database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, JSON, Float, DateTime
from sqlalchemy.orm import relationship
import datetime


class CryptoBase(Base):
    __tablename__ = "crypto_ohlc_daily"
    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    close_time = Column(DateTime, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    quote_volume = Column(Float, nullable=False)


