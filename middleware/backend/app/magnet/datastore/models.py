from magnet.database import Base
import sqlalchemy as sa


class CryptoPairs(Base):
    __tablename__ = "__crypto_pairs"
    id = sa.Column(sa.Integer, primary_key=True)
    provider = sa.Column(sa.String(255), nullable=False, default="")
    symbol = sa.Column(sa.String(255), nullable=False)


class CryptoBase:
    id = sa.Column(sa.Integer, primary_key=True)
    provider = sa.Column(sa.String(255), nullable=False, default="")
    market = sa.Column(sa.String(255), nullable=False)
    product = sa.Column(sa.String(255), nullable=False)
    periods = sa.Column(sa.Integer, nullable=False)


class CryptoOhlc(Base, CryptoBase):
    __tablename__ = "__crypto_ohlc_daily"
    close_time = sa.Column(sa.Date, nullable=False)
    open_price = sa.Column(sa.Float, nullable=False)
    high_price = sa.Column(sa.Float, nullable=False)
    low_price = sa.Column(sa.Float, nullable=False)
    close_price = sa.Column(sa.Float, nullable=False)
    volume = sa.Column(sa.Float, nullable=False)
    quote_volume = sa.Column(sa.Float, nullable=False)

    t_sma_5 = sa.Column(sa.Float, nullable=False, default=0)
    t_sma_10 = sa.Column(sa.Float, nullable=False, default=0)
    t_sma_15 = sa.Column(sa.Float, nullable=False, default=0)
    t_sma_20 = sa.Column(sa.Float, nullable=False, default=0)
    t_sma_25 = sa.Column(sa.Float, nullable=False, default=0)
    t_sma_30 = sa.Column(sa.Float, nullable=False, default=0)
    t_sma_200 = sa.Column(sa.Float, nullable=False, default=0)
    t_cross = sa.Column(sa.Integer, nullable=False, default=0, comment="1=golden cross -1=dead cross")

    __table_args__ = (
        sa.UniqueConstraint("provider", "market", "product", "periods", "close_time"),
        sa.Index("uix_query", "provider", "market", "product", "periods"),
        {'comment': '外部データソースから取得したチャート'}
    )


class CryptoTradeResult(Base, CryptoBase):
    __tablename__ = "crypto_trade_results"
    size = sa.Column(sa.DECIMAL, nullable=False)
    ask_or_bid = sa.Column(sa.Integer, nullable=False)
    entry_date = sa.Column(sa.DateTime, nullable=False)
    entry_close_date = sa.Column(sa.DateTime, nullable=False)
    entry_side = sa.Column(sa.String(255), nullable=False)
    entry_price = sa.Column(sa.DECIMAL, nullable=False)
    entry_commission = sa.Column(sa.DECIMAL, nullable=False)
    entry_reason = sa.Column(sa.String(255), nullable=False)
    settle_date = sa.Column(sa.DateTime, nullable=False)
    settle_close_date = sa.Column(sa.DateTime, nullable=False)
    settle_side = sa.Column(sa.String(255), nullable=False)
    settle_price = sa.Column(sa.DECIMAL, nullable=False)
    settle_commission = sa.Column(sa.DECIMAL, nullable=False)
    settle_reason = sa.Column(sa.String(255), nullable=False)
    job_name = sa.Column(sa.String(255), nullable=False)
    job_version = sa.Column(sa.String(255), nullable=False)
    is_back_test = sa.Column(sa.Boolean, nullable=False, default=False)
    close_date_interval = sa.Column(sa.Integer, nullable=False)
    diff_profit = sa.Column(sa.DECIMAL, nullable=False)
    diff_profit_rate = sa.Column(sa.DECIMAL, nullable=False)
    fact_profit = sa.Column(sa.DECIMAL, nullable=False)


class WebArchiveBase:
    id = sa.Column(sa.Integer, primary_key=True)
    referer = sa.Column(sa.String(1023), nullable=True)
    url = sa.Column(sa.String(1023), nullable=True)
    url_cache = sa.Column(sa.String(1023), nullable=True)
    title = sa.Column(sa.String(1023), nullable=True, default="")
    summary = sa.Column(sa.String(1023), nullable=True, default="")
    memo = sa.Column(sa.String(1023), nullable=False, default="")
    detail = sa.Column(sa.JSON, nullable=False, default={})


class Topic(Base, WebArchiveBase):
    __tablename__ = "__topic"

# https://news.livedoor.com/article/detail/18946401/
# コロナにより観光客が減ったため、奈良の鹿が鹿センベイを食べずにやせ細っている


# class Thread(Base, WebArchiveBase):
#     __tablename__ = "thread"


# class DataSource(Base, WebArchiveBase):
#     __tablename__ = "__datasource"
#     id = sa.Column(sa.Integer, primary_key=True, index=True)
#     url = sa.Column(sa.String(1023), nullable=True)
#     url_cache = sa.Column(sa.String(1023), nullable=True)
#     title = sa.Column(sa.String(1023), nullable=True, default="")
#     summary = sa.Column(sa.String(1023), nullable=True, default="")
#     memo = sa.Column(sa.String(1023), nullable=False, default="")
#     detail = sa.Column(sa.JSON, nullable=False, default={})

    # url = "http://www.scj.go.jp/ja/info/kohyo/year.html"  # 日本学術会議　提言　報告

