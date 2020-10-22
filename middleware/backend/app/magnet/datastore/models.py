from magnet.database import Base
import sqlalchemy as sa


class CryptoBase(Base):
    __tablename__ = "__crypto_ohlc_daily"
    id = sa.Column(sa.Integer, primary_key=True)
    provider = sa.Column(sa.String(255), nullable=False, default="")
    market = sa.Column(sa.String(255), nullable=False)
    product = sa.Column(sa.String(255), nullable=False)
    periods = sa.Column(sa.Integer, nullable=False)
    close_time = sa.Column(sa.DateTime, nullable=False)
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
        sa.UniqueConstraint(provider, market, product, periods, close_time, name="uix_price"),
        sa.Index("uix_query", provider, market, product, periods),
        {'comment': '外部データソースから取得したチャート'}
    )


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

