from magnet import Base
import sqlalchemy as sa


class TradeProfile(Base):
    __tablename__ = "trade_profile"
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.String(1024), nullable=False)
    provider = sa.Column(sa.String(255), nullable=False)
    market = sa.Column(sa.String(255), nullable=False)
    product = sa.Column(sa.String(255), nullable=False)
    periods = sa.Column(sa.Integer, nullable=False)
    cron = sa.Column(sa.String(255), nullable=False)
    broker = sa.Column(sa.String(255), nullable=False)
    order_id = sa.Column(sa.Float, nullable=True)
    trade_rule = sa.Column(sa.JSON, nullable=False, default={})

    __table_args__ = (
        sa.UniqueConstraint(name, name="uix_name"),
    )

